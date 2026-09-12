#!/usr/bin/env python3
"""
Telegram Bot for Alantik Antique Shop
Reads products from Google Sheets and posts to @alantiknw channel
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional
import asyncio

import telegram
from telegram.ext import Application, CommandHandler, ContextTypes
from google.oauth2.service_account import Credentials
from google.sheets.v4 import service as sheets_service
import gspread

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@alantiknw')
SHEET_ID = os.getenv('SHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME', 'Таблица1')
GCP_CREDENTIALS_JSON = os.getenv('GCP_CREDENTIALS_JSON')

# Google Sheets columns (adjust based on your sheet)
COLUMN_PHOTO_URL = 'A'
COLUMN_NAME = 'B'
COLUMN_DESCRIPTION = 'C'
COLUMN_PRICE = 'D'
COLUMN_STATUS = 'E'

class AlantikBot:
    def __init__(self):
        self.bot_token = TELEGRAM_TOKEN
        self.channel_id = CHANNEL_ID
        self.sheet_id = SHEET_ID
        self.sheet_name = SHEET_NAME
        
        # Initialize Google Sheets client
        try:
            creds_dict = json.loads(GCP_CREDENTIALS_JSON)
            credentials = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.gc = gspread.Authorize(credentials)
            self.sheet = self.gc.open_by_key(SHEET_ID)
            self.worksheet = self.sheet.worksheet(SHEET_NAME)
            logger.info("✅ Google Sheets connected successfully")
        except Exception as e:
            logger.error(f"❌ Error connecting to Google Sheets: {e}")
            raise
        
        # Initialize Telegram bot
        try:
            self.application = Application.builder().token(self.bot_token).build()
            self.bot = telegram.Bot(token=self.bot_token)
            logger.info("✅ Telegram bot initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing Telegram bot: {e}")
            raise
    
    def get_products(self) -> list:
        """Get all products from Google Sheets that are not yet published"""
        try:
            all_values = self.worksheet.get_all_records()
            products = []
            
            for idx, row in enumerate(all_values, start=2):  # start=2 because row 1 is header
                status = row.get('Статус', '').strip().lower()
                
                # Only process products that are not yet published
                if status != 'опубликовано':
                    product = {
                        'row_number': idx,
                        'photo_url': row.get('Фото (URL)', '').strip(),
                        'name': row.get('Название', '').strip(),
                        'description': row.get('Описание', '').strip(),
                        'price': row.get('Цена (RUB)', '').strip(),
                        'status': status
                    }
                    
                    # Only add if it has at least name and photo
                    if product['name'] and product['photo_url']:
                        products.append(product)
            
            return products
        except Exception as e:
            logger.error(f"❌ Error reading products from Sheets: {e}")
            return []
    
    def format_product_message(self, product: dict) -> str:
        """Format product data into a nice Telegram message"""
        message = f"""
✨ <b>{product['name']}</b>

📝 {product['description']}

💰 <b>{product['price']} ₽</b>

#антиквариат #мебель #винтаж #люстра #интерьер
        """.strip()
        return message
    
    async def post_product(self, product: dict) -> bool:
        """Post a single product to the Telegram channel"""
        try:
            message_text = self.format_product_message(product)
            
            # Post with photo
            await self.bot.send_photo(
                chat_id=self.channel_id,
                photo=product['photo_url'],
                caption=message_text,
                parse_mode='HTML'
            )
            
            logger.info(f"✅ Posted: {product['name']}")
            
            # Update status to "опубликовано"
            self.worksheet.update_cell(product['row_number'], 5, 'опубликовано')  # Column E = 5
            logger.info(f"✅ Updated status for row {product['row_number']}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Error posting product: {e}")
            return False
    
    async def post_all_products(self) -> None:
        """Post all new products to the channel"""
        products = self.get_products()
        
        if not products:
            logger.info("ℹ️ No new products to post")
            return
        
        logger.info(f"📤 Found {len(products)} new product(s) to post")
        
        for product in products:
            await self.post_product(product)
            # Add delay between posts to avoid rate limiting
            await asyncio.sleep(2)
    
    async def start_handler(self, update, context):
        """Handle /start command"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🤖 Alantik Bot is running!\n\nUse /post to post new products to @alantiknw"
        )
    
    async def post_handler(self, update, context):
        """Handle /post command"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⏳ Posting products..."
        )
        
        await self.post_all_products()
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="✅ Done! Posted all new products."
        )
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.application.add_handler(CommandHandler("start", self.start_handler))
        self.application.add_handler(CommandHandler("post", self.post_handler))
    
    async def run(self):
        """Run the bot"""
        self.setup_handlers()
        
        logger.info("🚀 Alantik Bot started!")
        logger.info(f"📢 Channel: {self.channel_id}")
        logger.info(f"📊 Sheet: {self.sheet_id}")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        
        try:
            # Run indefinitely (polling mode)
            await self.application.updater.start_polling()
            
            # Keep the bot running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

async def main():
    bot = AlantikBot()
    await bot.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
