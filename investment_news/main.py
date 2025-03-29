from datetime import datetime
from investment_list import get_investment_data, get_weekly_investments
from slack_sender import build_slack_block, send_to_slack
from credentials import SLACK_TOKEN, SLACK_CHANNEL

def main():
    """
    Main function to get weekly investments and send to Slack
    """
    try:
        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get investment data and filter for weekly investments
        investments = get_investment_data()
        weekly_investments = get_weekly_investments(investments, current_date)
        
        if not weekly_investments:
            print("No investment data found for the previous week")
            return
        
        # Build Slack blocks and send message
        blocks = build_slack_block(weekly_investments)
        if send_to_slack(SLACK_TOKEN, SLACK_CHANNEL, blocks):
            print("Successfully sent investment data to Slack")
        else:
            print("Failed to send message to Slack")
            
    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
