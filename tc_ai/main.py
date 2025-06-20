import functions_framework
from articles_list import get_techcrunch_ai_articles, filter_recent_articles
from gemini_summ import summarizer
from slack_sender import create_new_blocks, send_to_slack
import logging
from typing import List, Dict, Any
from credentials import SLACK_TOKEN, SLACK_CHANNEL

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_articles():
    """
    Main function to run the TechCrunch AI news pipeline:
    1. Get recent articles
    2. Generate summaries
    3. Send to Slack
    """
    articles = get_techcrunch_ai_articles()
    recent_articles = filter_recent_articles(articles)
    
    if not recent_articles:
        logger.info("No articles to send to Slack")
        return
    
    processed_articles = []
    for article in recent_articles:
        summary_result = summarizer(article['link'])
        if summary_result:
            processed_articles.append(summary_result)

    blocks = create_new_blocks(processed_articles)
    send_to_slack(blocks, SLACK_TOKEN, SLACK_CHANNEL)

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def main(event):
    process_articles()
