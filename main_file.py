import argparse
from datetime import datetime, date

from class_file import LinkedInApi
import pandas as pd

client_id = 'client_id'
client_secret = 'client_secret'
refresh_token = 'refresh_token'

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Script arguments')
    parser.add_argument('-s', '--start_date', required=False, help='Start date')
    parser.add_argument('-e', '--end_date', required=False, help='End date')
    return parser.parse_args()


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()


if __name__ == '__main__':

    # get passed in arguments
    args = parse_arguments()
    start_date = str_to_date(args.start_date) if args.start_date else None
    end_date = str_to_date(args.end_date) if args.end_date else None

    accounts_df = pd.read_csv('accounts.csv') #accounts.csv contains list of accounts (account_id, account_name) linked with LinkedIn Marketing App    
    account_ids = [r['account_id'] for _, r in accounts_df.iterrows()]

    client = LinkedInApi(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        start_date=start_date,
        end_date=end_date)

    # get campaign data    
    campaign_data = client.get_campaigns(account_ids)

    campaign_ids = [d['id'] for d in campaign_data]

    # get creative data
    creative_data = client.get_creatives(campaign_ids)

    creative_ids = [d['id'] for d in creative_data]

    # get tag data
    tag_data = client.get_third_party_tracking_tags(creative_ids)

    # get analytics data
    analytics_data = client.get_analytics(creative_ids)
