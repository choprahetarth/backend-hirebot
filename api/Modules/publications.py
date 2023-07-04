from scholarly import scholarly
from urllib.parse import urlparse
from urllib.parse import parse_qs

# confirming this logic instead of the website scraping one
# since it reached 300 concurrent requests paralelly, in stress testing


class Get_Published_Papers:
    def __init__(self, url):
        self.url = url

    def extract_papers(self):
        parsed_url = urlparse(self.url)
        captured_value = parse_qs(parsed_url.query)["user"][0]
        search_query = scholarly.search_author_id(captured_value, publication_limit=5)
        # Retrieve all the details for the author
        author = scholarly.fill(search_query, sortby="year")
        pubs = author["publications"][0:10]
        empty_string = ""
        for idx, value in enumerate(pubs):
            empty_string += str(idx) + " " + (value["bib"]["title"]) + "\n"
        return empty_string
