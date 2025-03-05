from paddleocr import PaddleOCR
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import gspread
from google.oauth2.service_account import Credentials

class PromptForBillExtractor:
    def __init__(self):
        self.prompts = {
            "product_name": "The name of the product which payment for. If it is just an individual transfer, the value is 'Chuyển tiền đến' + recipient's name.",
            "amount": "The amount of the transaction, in VND and may not be in standard form (eg 500k is 500,000). If not provided, the default value is 'N/A'",
            "payment_method": "The Payment method used in the transaction, use one of the options such as ['cash', 'banking', 'Momo']. If not provided, the default value is 'cash'.",
            "category": "The transaction category classification, use one of the options such as ['Thiết yếu', 'Giải trí', 'Đi lại', 'Ăn vặt', 'Sức khỏe', 'Mua sắm', 'Khác'].",
            "time": "The Transaction time with format %D/%M%Y. If not provided, return 'N/A'.",
            "snarky_comment": "A snarky comment to the user's transaction in Vietnamese. If the amount or product name are not provided, return a scolding message to user that this is not a transaction so you will not record it."
        }
    def get_response_schemas(self):
        return [ResponseSchema(name=key, description=desc) for key, desc in self.prompts.items()]

def extract_bill_text(image_path):
    ocr = PaddleOCR(lang="vi")
    results = ocr.ocr(image_path)
    return " ".join([line[1][0] for result in results for line in result])

def bill_parse(text:str, chat_model):
    prompt = PromptForBillExtractor()
    response_schemas = prompt.get_response_schemas()
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instruction = output_parser.get_format_instructions()
    template = """
    Extract the transaction information from the following text and format the output as JSON:
    {format_instruction}
    Text: {text}
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    message = prompt_template.format_messages(
        text=text,
        format_instruction=format_instruction
    )
    response = chat_model.invoke(message)
    return output_parser.parse(response.content)

def return_current_time():
    return datetime.now().strftime("%d/%m/%Y")

def parse_bill_from_text(text: str) -> dict:
    """Extract transaction information from text using a chat model."""
    chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    transaction = bill_parse(text=text, chat_model=chat_model)
    if transaction["time"] == "N/A":
        transaction["time"] = get_current_time()
    return transaction

def get_current_time() -> str:
    """Return the current time in the format %d/%m/%Y"""
    return datetime.now().strftime("%d/%m/%Y")
def extract_bill_from_image(image_path: str) -> dict:
    """Extract transaction information from an image."""
    text = extract_bill_text(image_path=image_path)
    return parse_bill_from_text(text=text)

def add_transaction_to_spreadsheet(
    product_name: str,
    amount: str,
    time: str,
    category: str,
    payment_method: str,
    note: str,
    worksheet: gspread.Worksheet
) -> None:
    """Add a transaction to the Google Sheets spreadsheet."""
    new_row = [product_name, amount, time, category, payment_method, note]
    worksheet.append_row(new_row)
