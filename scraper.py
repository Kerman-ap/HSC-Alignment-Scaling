import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

def scrape_marks(url, csv_filename="marks.csv"):
    """
    Scrapes the table from a rawmarks.info page and saves it as a CSV.
    Returns: csv_filename, formatted_title
    """
    response = requests.get(url)
    response.raise_for_status()  
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    header = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    data = []
    for row in rows[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            data.append(cols)
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    path = urlparse(url).path  
    title_part = path.strip("/").split("/")[-1] 
    formatted_title = " ".join(word.capitalize() for word in title_part.replace("-", " ").split())
    return csv_filename, formatted_title
