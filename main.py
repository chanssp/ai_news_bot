from huggingface_api import get_top_trending_models
from slack_sender import create_slack_blocks, send_to_slack
from credentials import SLACK_TOKEN, SLACK_CHANNEL

def main(limit: int):
    """
    Main function to fetch trending models and send them to Slack.
    
    Args:
        limit (int): Number of top trending models to fetch and display
    """
    # Get trending models
    trending_models = get_top_trending_models(limit=limit)
    if not trending_models:
        print("Failed to fetch trending models")
        return

    # Create and send Slack message
    blocks = create_slack_blocks(trending_models)
    if send_to_slack(SLACK_TOKEN, SLACK_CHANNEL, blocks):
        print(f"Successfully sent top {limit} trending models to Slack!")
    else:
        print("Failed to send message to Slack")

if __name__ == "__main__":
    # You can change this number to get more or fewer trending models
    main(limit=5)  # Example: Get top 10 trending models
