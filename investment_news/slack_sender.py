from typing import List, Any, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def build_slack_block(investments: List[Dict[str, str]]) -> List[Dict]:
    """
    Builds a Slack block message format from investment data
    
    Args:
        investments: List of investment dictionaries
    
    Returns:
        List of Slack blocks formatted according to Slack's Block Kit
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":rocket: 지난주 투자 유치 스타트업",
                "emoji": True
            }
        },
        {
            "type": "divider"
        }
    ]

    # Build text string with all investments
    text = ""
    for inv in investments:
        text += f"• *{inv['name']}*: {inv['domain']}, {inv['amount']}, {inv['stage']}, [{inv['houses']}]\n"

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    })

    return blocks

def send_to_slack(token: str, channel: str, blocks: List[Dict[str, Any]]) -> bool:
    """
    Send formatted blocks to Slack channel.
    """
    client = WebClient(token=token)

    try:
        client.chat_postMessage(
            channel=channel,
            blocks=blocks
        )
        return True
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return False 