import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_latest_briefing_url() -> Optional[str]:
    """
    AI타임스의 뉴스 브리핑 섹션에서 가장 최신 기사의 URL을 추출합니다.
    
    Returns:
        str or None: 최신 기사의 URL. 실패시 None 반환
    """
    url = "https://www.aitimes.com/news/articleList.html"
    params = {
        "sc_sub_section_code": "S2N110",
        "view_type": "sm"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        section_list = soup.find('section', id='section-list')
        
        if not section_list:
            logger.error("Could not find section-list element")
            return None
            
        # 첫 번째 기사 링크 찾기
        first_article = section_list.find('a')
        
        if first_article and 'href' in first_article.attrs:
            article_url = first_article['href']
            if not article_url.startswith('http'):
                article_url = f"https://www.aitimes.com{article_url}"
                
            logger.info(f"Found latest article: {first_article.text.strip()}")
            logger.info(f"URL: {article_url}")
            return article_url
        else:
            logger.error("No article link found in section-list")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Failed to fetch the webpage: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while processing the webpage: {e}")
        logger.exception(e)
        return None
