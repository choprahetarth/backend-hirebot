from pypdf import PdfReader


class Pdf_Scrape:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def scrape(self, max_length=2):
        reader = PdfReader(self.input)
        output_text = ""
        number_of_pages = len(reader.pages)
        min_length = min(number_of_pages, max_length)
        for i in range(min_length):
            page = reader.pages[i]
            text = page.extract_text()
            output_text = output_text + text + " "
        return output_text

    def save_text(self, text):
        with open(self.output, "w") as f:
            f.write(text)