from urllib.request import urlopen
from bs4 import BeautifulSoup


class Website_Scrape:
    def __init__(self, url, path):
        self.url = url
        self.path = path

    def scrape(self):
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # # drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text

    def save_text(self, text):
        with open(self.path, "w") as f:
            f.write(text)


if __name__ == '__main__':

    c = Website_Scrape('https://haohanwang.github.io/publications.html','./publications.txt')
    text = c.scrape()
    c.save_text(text)


    c = Website_Scrape('https://haohanwang.github.io/','./professor.txt')
    text = c.scrape()
    c.save_text(text)