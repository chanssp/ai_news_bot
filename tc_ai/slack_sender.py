from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from credentials import SLACK_TOKEN, SLACK_CHANNEL

def create_new_blocks(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Create Slack message blocks for TechCrunch AI articles.
    
    Args:
        articles (List[Dict]): List of article dictionaries containing 'title', 'summary', and 'url'
    
    Returns:
        List[Dict[str, Any]]: Formatted Slack blocks
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🤖 TechCrunch 오늘의 AI 기사 ({date_str})",
                "emoji": True
            }
        },
        {
            "type": "divider"
        }
    ]

    # Add each article as a section
    for article in articles:
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{article['url']}|{article['title']}>*\n{article['summary']}"
                }
            },
            {
                "type": "divider"
            }
        ])

    # Add footer
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "👉 <https://techcrunch.com/category/artificial-intelligence/|TechCrunch AI 기사 전체 보기>"
            }
        ]
    })

    return blocks

def send_to_slack(blocks: List[Dict[str, Any]], token: str, channel: str) -> bool:
    """
    Send formatted blocks to Slack channel.
    
    Args:
        blocks (List[Dict[str, Any]]): Formatted Slack blocks to send
        token (str): Slack bot token (default from credentials)
        channel (str): Target Slack channel (default from credentials)
    
    Returns:
        bool: True if successful, False otherwise
    """
    client = WebClient(token=token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            unfurl_links=False,
            unfurl_media=False
        )
        return True
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return False

if __name__ == "__main__":
    # Test the functions with a sample article
    test_articles = [{
        "title": "Test Article",
        "summary": "This is a test summary of the article that demonstrates the new format.",
        "url": "https://techcrunch.com/test"
    }]
    
    blocks = create_new_blocks(test_articles)
    success = send_to_slack(blocks)
    print(f"Message sent successfully: {success}")
