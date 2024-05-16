# Load the Google Search Console API credentials
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')

# Create Google Search Console API client
credentials = google.oauth2.credentials.Credentials(
    None,
    refresh_token=GOOGLE_REFRESH_TOKEN,
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    token_uri='https://accounts.google.com/o/oauth2/token'
)
webmasters_service = build('webmasters', 'v3', credentials=credentials)

def fetch_top_queries(keyword):
    site_url = 'https://www.yourwebsite.com/'  # Replace with your website URL
    request = {
        'startDate': '7daysAgo',  # Adjust the date range as needed
        'endDate': 'today',
        'dimensions': ['query'],
        'rowLimit': 10,
        'dimensionFilterGroups': [
            {
                'filters': [
                    {
                        'dimension': 'query',
                        'operator': 'CONTAINS',
                        'expression': keyword
                    }
                ]
            }
        ]
    }
    response = webmasters_service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    top_queries = [row['keys'][0] for row in response['rows']]
    return top_queries