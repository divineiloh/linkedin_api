from linkedin_api.clients.auth.client import AuthClient
from linkedin_api.clients.restli.client import RestliClient
from datetime import date, timedelta
import pandas as pd

class LinkedInApi():

    def __init__(
            self,
            client_id,
            client_secret,
            refresh_token,
            start_date = None,
            end_date = None):

        auth_client = AuthClient(client_id, client_secret)
        r = auth_client.exchange_refresh_token_for_access_token(refresh_token)

        self.access_token = r.access_token
        self.client = RestliClient()
        yesterday = date.today() - timedelta(days=1)
        self.start_date = start_date if start_date else yesterday
        self.end_date = end_date if end_date else yesterday
        print(f'API initialized for {self.start_date} to {self.end_date}')


    def daterange(self) -> date:
        """
        returns each date between start and end
        """
        for n in range(int((self.end_date - self.start_date).days)+1):
            yield self.start_date + timedelta(n)


    def split_list(self, data: list, batch_size: int, prefix: str = '') -> list:
        for n in range(0, len(data), batch_size):
            # print(f'Range {n} to {n+batch_size}')
            yield [f'{prefix}{d}' for d in data[n:n+batch_size]]


    def check_status(self, resp):
        if resp.status_code != 200:
            raise Exception(f'Response code is {resp.status_code}. {resp.response.text}')
        
        print(f'Retrieved {len(resp.elements) if resp.elements else 0} entries')


    def get_campaigns(self, account_ids: list) -> list:
        """
        Get campaign data from account_ids
        """
        print('Getting campaigns')
        query_values = [f'urn:li:sponsoredAccount:{a}' for a in account_ids]

        r = self.client.finder(
            resource_path='/adCampaignsV2',
            finder_name='search',
            query_params={
                'search': {
                    'account': {'values': query_values},
                },
  
            },
            access_token=self.access_token)

        self.check_status(r)

        return r.elements
        
        #print(r.response.text)


    def get_creatives(self, campaign_ids: list, batch_size: int = 20) -> list:
        """
        Get creative data from campaign_ids
        """
        print('Getting creatives')
        prefix = 'urn:li:sponsoredCampaign:'
        output = []

        # split_list lets us split a big list into small pieces
        for query_values in self.split_list(campaign_ids, batch_size, prefix):
            r = self.client.finder(
                resource_path='/adCreativesV2',
                finder_name='search',
                query_params={
                    'search': {
                        'campaign': {'values': query_values},
                    },
                },
                access_token=self.access_token)
            
            self.check_status(r)
        
            output.extend(r.elements)

        return output


    def get_third_party_tracking_tags(self, creative_ids: list) -> list:
        """
        Get tracking tags from creative_ids
        """
        print('Getting tracking tags')
        prefix = 'urn:li:sponsoredCreative:'
        output = []
        
        for query_values in self.split_list(creative_ids, 1, prefix):
            r = self.client.finder(
                resource_path='/thirdPartyTrackingTags',
                finder_name='creative',
                query_params={
                    'creative': query_values[0],
                },
                access_token=self.access_token)
            
            self.check_status(r)
        
            output.extend(r.elements)

        return output


    def get_analytics(self, creative_ids: list, batch_size: int = 20) -> list:
        """
        Get daily analytics data from creative_ids
        """
        print('Getting analytics')
        prefix = 'urn:li:sponsoredCreative:'
        key_fields = ['pivotValues']
        fields = [
            'dateRange',
            'approximateUniqueImpressions',
            'clicks',
            'comments',
            'conversionValueInLocalCurrency',
            'costInLocalCurrency',
            'externalWebsiteConversions',
            'externalWebsitePostClickConversions',
            'externalWebsitePostViewConversions',
            'follows',
            'impressions',
            'landingPageClicks',
            'oneClickLeadFormOpens',
            'oneClickLeads',
            'reactions',
            'shares',
            'videoCompletions',
            'videoFirstQuartileCompletions',
            'videoMidpointCompletions',
            'videoThirdQuartileCompletions',
            'videoViews',
        ]
        field_batch_size = 15 # API has a 20 field limitation
        output = []
        for n in range(((len(fields)-1)//field_batch_size)+1):
            output.append([])
        
        for each_day in self.daterange():
            print(f'Processing {each_day}')

            for query_values in self.split_list(creative_ids, batch_size, prefix):
                field_counter = 0
                for field_values in self.split_list(fields, field_batch_size):
        
                    r = self.client.finder(
                        resource_path='/adAnalyticsV2',
                        finder_name='analytics',
                        query_params={
                            'dateRange': {
                                'start': {
                                    'day': each_day.day,
                                    'month': each_day.month,
                                    'year': each_day.year},
                                'end': {
                                    'day': each_day.day,
                                    'month': each_day.month,
                                    'year': each_day.year},
                            },
                            'creatives': query_values,
                            'timeGranularity': 'DAILY',
                            'pivot': 'CREATIVE',
                            'fields':','.join(key_fields + field_values),
                        },
                        access_token=self.access_token)
            
                    self.check_status(r)
        
                    output[field_counter].extend(r.elements)
                    field_counter += 1

        # print(output)

        # format and merge output
        main_df = None
        for o in range(len(output)):
            for row in range(len(output[o])):
                output[o][row]['pivotValues'] = output[o][row]['pivotValues'][0]
                if 'dateRange' in output[o][row]:
                    output[o][row]['dateRange'] = date(
                        output[o][row]['dateRange']['start']['year'],
                        output[o][row]['dateRange']['start']['month'],
                        output[o][row]['dateRange']['start']['day'])

            if output[o]:
                if o == 0:
                    main_df = pd.DataFrame.from_records(output[o])
                    main_df['pivotValues'] = main_df['pivotValues'].astype(str)
                    main_df.set_index('pivotValues', drop=False, inplace=True)
                else:
                    df = pd.DataFrame.from_records(output[o])
                    df['pivotValues'] = df['pivotValues'].astype(str)
                    df.set_index('pivotValues', inplace=True)
    
                    main_df = pd.merge(
                        main_df,
                        df,
                        how='left',
                        left_index=True,
                        right_index=True)
            
        return main_df.to_dict('records')
