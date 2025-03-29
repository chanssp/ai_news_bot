import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict
from datetime import datetime, timedelta

def get_investment_data() -> List[Dict[str, str]]:
    """
    Scrapes investment data from startuprecipe.co.kr/invest
    Returns a list of dictionaries containing investment information
    """
    url = "https://startuprecipe.co.kr/invest"
    
    try:
        # Send request with headers to mimic browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table
        table = soup.select_one('div.dataTables_wrapper table#example')
        if not table:
            raise ValueError("Table not found on the page")
            
        # Get all rows except header
        rows = table.find_all('tr')[1:]  # Skip header row
        
        investments = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 6:  # Ensure row has all required cells
                investment = {
                    "date": cells[0].get_text(strip=True) or "",
                    "name": cells[1].get_text(strip=True) or "",
                    "domain": cells[2].get_text(strip=True) or "",
                    "amount": cells[3].get_text(strip=True) or "",
                    "stage": cells[4].get_text(strip=True) or "",
                    "houses": cells[5].get_text(strip=True) or ""
                }
                investments.append(investment)
        
        return investments
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"Error processing data: {e}")
        return []

def get_weekly_investments(investments: List[Dict[str, str]], date: str) -> List[Dict[str, str]]:
    """
    Get the investment data for the previous week of the given date
    
    Args:
        investments: List of investment dictionaries
        date: Date string in format 'YYYY-MM-DD'
    
    Returns:
        List of investments from the previous week
    """
    current_date = datetime.strptime(date, '%Y-%m-%d')
        
    try:
        # Convert input date to datetime
        current_date = datetime.strptime(date, '%Y-%m-%d')
        
        # Calculate the start and end dates for the previous week
        end_date = current_date - timedelta(days=1)  # Previous day
        start_date = end_date - timedelta(days=6)  # 7 days before end_date
        
        # Filter investments within the date range
        weekly_investments = [
            inv for inv in investments
            if start_date <= datetime.strptime(inv["date"], '%Y-%m-%d') <= end_date
        ]
        
        return weekly_investments
        
    except ValueError as e:
        print(f"Error processing date: {e}")
        return []
    except Exception as e:
        print(f"Error getting weekly investments: {e}")
        return []
