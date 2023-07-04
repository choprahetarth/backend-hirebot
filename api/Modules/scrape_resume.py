from pypdf import PdfReader
from io import BytesIO
import re
import string


def clean_text(text):
    "Apply preprocessing techniques on the text data"
    # Convert text to lower case
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # remove multiple spaces
    text = re.sub(' +', ' ', text)
    # remove newline characters
    text = re.sub(r'\s*\n\s*', ' ', text.strip())
    # Remove tabs
    text = text.replace('\t', ' ')
    # Remove any text inside the square brackets
    text = re.sub(r'\[[^]]*\]', '', text)
    # Remove URL's
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Remove all digits
    text = re.sub(r'\d', '', text)
    return text


def scrape_resume(file_in_memory):
    reader = PdfReader(BytesIO(file_in_memory.read()))
    output_text = ""
    number_of_pages = min(len(reader.pages), 2)
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        output_text = output_text + text + " "
    cleaned_text = clean_text(output_text)
    return cleaned_text
