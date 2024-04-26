from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
from config import config
from nlp.openai_client import OpenAIClient

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

def better_keyword_research(list_of_keywords, keyword):
    oa = OpenAIClient(config.OPENAI_LLM_BEST_MODEL, 0, True)

    list_of_keywords_str = str(list_of_keywords)

    better_keyword_prompt = f'''
        Given the main keyword "{keyword}", and a list of potential related keywords, select keywords from this list that can be used to expand on the topic in a single comprehensive article. Output the selected keywords in JSON format.
        Ensure that the selected keywords are diverse and cover different aspects or details about the topic, suitable for creating sections within the article. Match the search intent of the main keyword, focusing on what users are most likely to seek regarding this topic.
        Exclude any repetitive or overly similar variations of the keyword that wouldn't add significant new information or perspective to the article.
    '''

    oa.add_to_message(better_keyword_prompt, 'system')
    oa.add_to_message(list_of_keywords_str, 'user')

    return oa.completions()