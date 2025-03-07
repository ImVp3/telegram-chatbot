from telegram.ext import * 
from telegram import Update
import os
from dotenv import load_dotenv, find_dotenv
from utils import parse_bill_from_text, extract_bill_from_image, add_transaction_to_spreadsheet
import gspread
from google.oauth2.service_account import Credentials

load_dotenv(find_dotenv())

creds = Credentials.from_service_account_file("credentials.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
spreadsheet  = "1CRqmq1mhXGVcG4iIgGXQ7zZ3fLnlY6G5-TzxEXPbtrw"
spreadsheet  = client.open_by_key(spreadsheet )
worksheet = spreadsheet.worksheet("transactions")

async def start_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello, i am a dump bot")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming text messages, extracting transactions and adding them to the Google Sheets database."""
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        image_path = os.path.join("data", f"{photo.file_id}.jpg")
        await file.download_to_drive(image_path)
        response = extract_bill_from_image(image_path)
    else:
        response = parse_bill_from_text(update.message.text)

    if response["product_name"] != "N/A" and response["amount"] != "N/A":
        add_transaction_to_spreadsheet(
            product_name=response["product_name"],
            amount=response["amount"],
            time=response["time"],
            category=response["category"],
            payment_method=response["payment_method"],
            note="",
            worksheet=worksheet
        )

    await update.message.reply_text(response["snarky_comment"])



async def handle_error(update, context):
    pass

if __name__ == "__main__":   
    print("starting")
    app = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()
    
    app.add_handler( CommandHandler('start', start_command))
    
    app.add_handler(MessageHandler(filters.ALL, handle_message))
        
    print("Rolling")
    app.run_polling(poll_interval=2)