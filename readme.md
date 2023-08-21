# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Documentation for Script- LinkedIn Ad Insights API Python Script (LinkedIn_API.py)
# Version - v1.0
# Update Date - August 1 2023
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------
# --------------------------------------1. Pre-requisites---------------------------------------
# ----------------------------------------------------------------------------------------------

The following files must be placed in the directory from which LinkedIn_API.py would be executed:

1. account_ids.csv : This csv contains list of accounts (account_id, account_name) linked with LinkedIn Marketing App 
	{Account_ids needs to be manually checked for new accounts added to the App}
2. LinkedIn_API.py : This is the Python script which calls the LinkedIn API to extract ad metrics data

# ----------------------------------------------------------------------------------------------
# -------------------------------------2. Execution Steps---------------------------------------
# ----------------------------------------------------------------------------------------------	

There are two modes of operation :

1. Default Mode: This generates a csv with ad metric values of all Active ads for 'yesterday' 
	(Eg: If run on 2022/01/10, it will generate metric values for 2022/01/09)
	For executing from terminal, type in the following from the directory in which the csv and .py file is placed:
	>> python LinkedIn_API.py account_ids.csv Current
	
2. Backfill Mode: This generates a csv with ad metric values of all ads in the mentioned time range. The user will be prompted for a Start Date and End Date.
	(Eg: If run on 2022/01/10, with Start_Date: 2021-01-01 and End_Date: 2021-12-31, it will generate metric values for all days between 2021/01/01 and 2021/12/31)
	For executing from terminal, type in the following from the directory in which the 2 csv's and .py file is placed:
	>> python LinkedIn_API.py account_ids.csv Backfill
	
	Enter the Start Date(YYYY-MM-DD) and End Date (YYYY-MM-DD)
	
	Start Date: <your_input>
	End Date: <your_input>


# ----------------------------------------------------------------------------------------------
# -------------------------------------3. Outputs generated-------------------------------------
# ----------------------------------------------------------------------------------------------

4 CSVs with these attributes at a daily level for all ads. The variable description is as follows:

1. account_id : Unique Identifier for the advertising account
2. account_name : Name of the account (A club may have multiple account names)
3. campaign_id : Numerical Identifier for the campaign
4. campaign_name : Name of the campaign
5. campaign_objective_type : Objective type of campaign
6. campaign_status : Status of campaign
7. campaign_type : Type of campaign
8. ad_id : Id of ad form
9. ad_name : Name of the ad
10. ad_objective_type : Objective type of ad
11. click_url : Count of clicks on any links (anchor tags)
12. total_spent : USD spent on ad
13. impressions : Count of impressions for Direct Ads, Sponsored Updates, 'sends' for InMails
14. views : A video ad playing for at least 2 continuous seconds 50% in-view, or a click on the CTA, whichever comes first. An interaction with the video (like going to fullscreen mode) does not count as a view
15. views_25% : The count of video ads that played through the first quartile of the video. This includes watches that skipped to this point if the serving location is ON_SITE
16. views_50% : The count of video ads that played through the midpoint of the video. This includes watches that skippped to this point if the serving location is ON_SITE
17. views_75% : The count of video ads that played through the third quartile of the video. This includes watches that skipped to this point if the serving location is ON_SITE
18. completions : The count of video ads that played 97-100% of the video. This includes watches that skipped to this point if the serving location is ON_SITE
19.	leads : The count of leads generated through One Click Lead Gen
20. leads_forms_opened : The count of times users opened the lead form for a One Click Lead Gen campaign
21. clicks : Count of chargeable clicks
22. reactions : The count of positive reactions on Sponsored Updates which can capture, like, interest, praise, and other responses
23. comments : The count of comments. Sponsored Updates only
24. shares : The count of shares. Sponsored Updates only
25. follows : The count of follows. Sponsored Updates only
26. landing_page_clicks : The count of clicks which take the user to the creative landing page
27. conversions : The count of conversions indicated by pixel loads
28. reach : The approximate reach of the campaign
29. post_click_conversions : The count of post-click conversions indicated by pixel loads
30. view_through_conversions : The count of view conversions indicated by pixel loads
31. total_conversion_value : The total value of all conversions
32. date : The date for which metrics have been fetched (In MM-DD-YYYY HH:mm:ss format)
33. tracking_url_CLICK : The tracking url tagged for type 'Click'
34. tracking_url_IMPRESSION : The tracking url tagged for type 'Impressions'
