import logging
from news_briefing import get_latest_briefing_url
from article_parse import extract_article_paragraphs, split_article_content
from gemini_summarizer import summarize_text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_and_print_latest_article():
    """
    최신 뉴스 브리핑 기사를 가져와서 출력합니다.
    """
    # 1. 최신 기사 URL 가져오기
    article_url = get_latest_briefing_url()
    if not article_url:
        logger.error("Failed to get the latest article URL")
        return
    
    logger.info(f"Latest article URL: {article_url}")
    
    # 2. 기사 내용 파싱
    paragraphs = extract_article_paragraphs(article_url)
    
    # 3. 결과 출력
    if paragraphs is not None:
        if paragraphs:
            # 기사 내용 분리
            intro, news = split_article_content(paragraphs)
            
            # 소개 부분 요약
            intro_text = ' '.join(intro)  # 문단들을 하나의 텍스트로 합치기
            summary = summarize_text(intro_text)
            
            print("\n=== 브리핑 소개 요약 ===")
            print("-" * 50)
            print(f"{summary}\n")
                
            print("\n=== 주요 뉴스 ===")
            print("-" * 50)
            for para in news:
                print(f"{para}\n")
            print("-" * 50)
        else:
            logger.warning("No content found in the article")
    else:
        logger.error("Failed to parse the article content")

if __name__ == "__main__":
    fetch_and_print_latest_article()
