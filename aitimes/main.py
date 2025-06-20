import functions_framework
import logging
from news_briefing import get_latest_briefing_url
from article_parse import extract_article_paragraphs, split_article_content
from gemini_summarizer import summarize_text
from slack_sender import create_news_blocks, send_to_slack
from credentials import SLACK_TOKEN, SLACK_CHANNEL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_and_print_latest_article():
    """
    최신 뉴스 브리핑 기사를 가져와서 출력하고 슬랙으로 전송합니다.
    """
    # 1. 최신 기사 URL 가져오기
    article_url = get_latest_briefing_url()
    if not article_url:
        logger.error("Failed to get the latest article URL")
        return
    
    logger.info(f"Latest article URL: {article_url}")
    
    # 2. 기사 내용 파싱
    paragraphs = extract_article_paragraphs(article_url)
    
    # 3. 결과 처리
    if paragraphs:
        # 기사 내용 분리
        intro, news = split_article_content(paragraphs)
        
        # 소개 부분 요약
        intro_text = ' '.join(intro)  # 문단들을 하나의 텍스트로 합치기
        summary = summarize_text(intro_text)
        
        # 슬랙으로 전송
        blocks = create_news_blocks(summary, news, article_url)
        if send_to_slack(SLACK_TOKEN, SLACK_CHANNEL, blocks):
            logger.info("Successfully sent message to Slack")
        else:
            logger.error("Failed to send message to Slack")
    else:
        logger.error("Failed to parse the article content")

@functions_framework.cloud_event
def main(event):
    fetch_and_print_latest_article()
