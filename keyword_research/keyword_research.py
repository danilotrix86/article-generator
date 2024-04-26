from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
from config import config

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes, 'Content-Encoding' : 'gzip'}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)

def keyword_research(keyword, language, location):
    
        client = RestClient(config.DATA_FOR_SEO_EMAIL, config.DATA_FOR_SEO_PASSWORD)
        post_data = dict()
        # simple way to set a task
        post_data[len(post_data)] = dict(
        keyword=keyword,
        location_name=location,
        language_name=language,
        filters=[
                ["keyword_data.keyword_info.search_volume", ">", 10]
        ],
        limit=3
        )
        # POST /v3/dataforseo_labs/google/related_keywords/live
        response = client.post("/v3/dataforseo_labs/google/related_keywords/live", post_data)
        
        keywords_with_related = []

        # Loop through each task's result items and extract keywords along with related keywords
        for task in response['tasks']:
            for item in task['result'][0]['items']:
                keyword_entry = {
                    'keyword': item['keyword_data']['keyword'],
                    'related_keywords': item['related_keywords']
                }
                keywords_with_related.append(keyword_entry)

        # Now 'keywords_with_related' contains all the primary keywords and their related keywords
        return keywords_with_related