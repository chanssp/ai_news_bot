import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from dateutil import parser
import pytz

def get_techcrunch_ai_articles():
    url = "https://techcrunch.com/category/artificial-intelligence/"
    
    try:
        # Send request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the article list container
        article_list = soup.find('ul', {'data-wp-class--force-hide': 'state.showDefaultComponents'})
        
        articles = []
        if article_list:
            # Find all article items
            for article in article_list.find_all('li', class_='wp-block-post'):
                # Extract title
                title_element = article.find('h3', class_='loop-card__title')
                title = title_element.text.strip() if title_element else None
                
                # Extract link
                link_element = title_element.find('a') if title_element else None
                link = link_element['href'] if link_element else None
                
                # Extract upload time and convert to UTC
                meta_element = article.find('div', class_='loop-card__meta')
                time_element = meta_element.find('time') if meta_element else None
                local_time = time_element['datetime'] if time_element else None
                
                # Convert to UTC if time exists
                upload_time = None
                if local_time:
                    dt = parser.parse(local_time)
                    utc_time = dt.astimezone(pytz.UTC)
                    upload_time = utc_time.isoformat()
                
                if title and link:
                    articles.append({
                        'title': title,
                        'link': link,
                        'upload_time': upload_time
                    })
        
        return articles
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def filter_recent_articles(articles, hours=24):
    """
    Filter articles that were published within the specified number of hours (default 24).
    
    Args:
        articles (list): List of article dictionaries containing 'upload_time'
        hours (int): Number of hours to look back (default 24)
    
    Returns:
        list: Filtered list of articles within the specified time window
    """
    now = datetime.now(pytz.UTC)
    time_threshold = now - timedelta(hours=hours)
    
    recent_articles = []
    for article in articles:
        if article['upload_time']:
            article_time = parser.parse(article['upload_time'])
            if article_time >= time_threshold:
                recent_articles.append(article)
    
    return recent_articles

if __name__ == "__main__":
    # Get articles
    articles = get_techcrunch_ai_articles()
    
    # Filter for recent articles
    recent_articles = filter_recent_articles(articles)
    
    # Print results in a formatted way
    print(json.dumps(recent_articles, indent=2)) 