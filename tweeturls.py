import requests
import re
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from datetime import datetime

def get_oembed_html(url):
    """ Fetch HTML for a tweet using Twitter oEmbed API. """
    oembed_url = f"https://publish.twitter.com/oembed?url={url}"
    response = requests.get(oembed_url)
    if response.status_code == 200:
        return response.json().get("html", "")
    else:
        return None

def extract_content(html_content):
    """ Extracts and formats content from HTML. """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extracting tweet text
    tweet_text = soup.find('p').get_text(strip=True) if soup.find('p') else "No text"
    
    # Extracting author and date
    author_info = soup.find('blockquote').get_text(strip=True)
    author = re.search(r'—\s(.*?)\s\(', author_info)
    date = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b', author_info)

    author = author.group(1).strip() if author else "Unknown_author"
    date = date.group(0) if date else "Unknown_date"

    # Convert date to YYYY_MM_DD format
    if date != "Unknown_date":
        date = datetime.strptime(date, '%B %d, %Y').strftime('%Y_%m_%d')

    # Extracting URL
    tweet_url = soup.find('a')['href'] if soup.find('a') else "No URL"

    return f"{date} {author}\n{tweet_text}\n{tweet_url}\n"



def main():
    with open("urls.txt", "r") as file:
        urls = file.readlines()

    with open("output.md", "w") as file:
        for url in urls:
            url = url.strip()
            html_content = get_oembed_html(url)
            if html_content:
                formatted_content = extract_content(html_content)
                file.write(formatted_content + "\n")

if __name__ == "__main__":
    main()
