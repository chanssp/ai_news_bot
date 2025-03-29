from typing import Dict, Any, List
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def create_slack_blocks(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Create formatted Slack blocks for the trending models.
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🤗 Hugging Face Trending Models 순위 " + datetime.now().strftime("%Y-%m-%d"),
                "emoji": True
            }
        },
        {
            "type": "divider"
        }
    ]

    for model in models:
        text_content = f"{model['likes']} likes | {model['downloads']} downloads | {model['lastModified']}"
        if 'pipeline_tag' in model:
            text_content = f"*{model['pipeline_tag']}* | {text_content}"

        model_block = {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": f"{model['avatarUrl']}",
                    "alt_text": "- "
                },
                {
                    "type": "mrkdwn",
                    "text": f"*{model['id']}*",
                },
                {
                    "type": "mrkdwn",
                    "text": text_content
                }
            ]
        }

        blocks.append(model_block)
        blocks.append({"type": "divider"})

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