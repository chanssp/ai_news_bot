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

def process_articles() -> List[Dict[str, Any]]:
    """
    Process articles through the pipeline:
    1. Get recent articles
    2. Generate summaries
    3. Return processed articles
    """
    # Get recent articles
    logger.info("Fetching TechCrunch AI articles...")
    articles = get_techcrunch_ai_articles()
    recent_articles = filter_recent_articles(articles)
    
    if not recent_articles:
        logger.info("No recent articles found")
        return []
    
    logger.info(f"Found {len(recent_articles)} recent articles")
    
    # Process each article through Gemini
    processed_articles = []
    for article in recent_articles:
        logger.info(f"Generating summary for article: {article['title']}")
        try:
            summary_result = summarizer(article['link'])
            if summary_result:
                processed_articles.append(summary_result)
            else:
                logger.warning(f"Failed to generate summary for article: {article['title']}")
        except Exception as e:
            logger.error(f"Error processing article {article['title']}: {str(e)}")
    
    return processed_articles

def main():
    """
    Main function to run the TechCrunch AI news pipeline
    """
    try:
        # Process articles
        processed_articles = process_articles()
        
        if not processed_articles:
            logger.info("No articles to send to Slack")
            return
        
        # Create and send Slack message
        logger.info("Creating Slack message blocks...")
        blocks = create_new_blocks(processed_articles)
        
        logger.info("Sending to Slack...")
        success = send_to_slack(blocks, SLACK_TOKEN, SLACK_CHANNEL)
        
        if success:
            logger.info("Successfully sent message to Slack")
        else:
            logger.error("Failed to send message to Slack")
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main()
