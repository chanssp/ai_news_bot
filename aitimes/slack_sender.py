from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def create_news_blocks(summary: str, news_items: List[str], article_url: str) -> List[Dict[str, Any]]:
    """
    브리핑 소개와 주요 뉴스를 포함하는 슬랙 메시지 블록을 생성합니다.
    
    Args:
        summary (str): 브리핑 소개 요약
        news_items (List[str]): 주요 뉴스 항목 리스트
        article_url (str): 원본 기사 URL
    
    Returns:
        List[Dict[str, Any]]: 슬랙 블록 메시지 포맷
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🔥 AI타임스 뉴스 브리핑",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": summary
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*📰 주요 뉴스*"
            }
        }
    ]
    
    # 주요 뉴스 항목 추가
    for item in news_items:
        if item.strip():  # 빈 항목 제외
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": item
                }
            })
    
    # 원본 기사 링크 추가
    blocks.extend([
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"👉 <{article_url}|원본 기사 보기>"
                }
            ]
        }
    ])
    
    return blocks

def send_to_slack(token: str, channel: str, blocks: List[Dict[str, Any]]) -> bool:
    """
    Send formatted blocks to Slack channel.
    """
    client = WebClient(token=token)

    try:
        client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            unfurl_links=False,
            unfurl_media=False
        )
        return True
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return False
