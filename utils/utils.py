from openai import OpenAI
from config import config 
import json


client = OpenAI(api_key=config.OPENAI_API_KEY)


def extract_json(model, keywords, secondary_keyword, third_keyword, brief, language, h2_count, h3_count, raw_content, search_intent):

    print ("Extracting JSON structure...")
    try:
        response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f'''
                
                You are a helpful assistant tasked with creating structured content for articles using search intent. 
                When provided with a keyword or a list of keywords, your task is to return a nested JSON structure*. 
                This structure should clearly reflect a hierarchy suitable for an article, with an 'H1' tag for the title of the article, 'H2' tags for main sections or subtitles, and 'H3' tags for subsections under each H2. 
                Here is the correct format you should follow to return the JSON:

                {{
                "title": "Title of H1 article",
                "subsections": [
                    {{
                    "title": "Title of first H2 article",
                    "subsections": [
                        {{
                        "title": "Title of first H3 article under first H2"
                        }},
                        {{
                        "title": "Title of second H3 article under first H2"
                        }}
                    ]
                    }},
                    {{
                    "title": "Title of second H2 article",
                    "subsections": [
                        {{
                        "title": "Title of first H3 article under second H2"
                        }},
                        {{
                        "title": "Title of second H3 article under second H2"
                        }},
                        {{
                        "title": "Title of third H3 article under second H2"
                        }}
                    ]
                    }}
                ]
                }}


                Ensure the structure you create follows this example, with 'H1' for the article's main title, followed by at least {h2_count} 'H2' for each main section or subtitle, and at least {h3_count} 'H3' for subsections within those sections. 
                Please create a nested JSON structure based on the main keyword provided, accurately reflecting this hierarchy.

            
                '''
            },
            {"role": "user", "content": f"The main keywords for the article are: {keywords}, secondary keyword is {secondary_keyword} and {third_keyword} and this is the brief: {brief}. {raw_content}. Please return a nested JSON structure* based on the information provided. Write the JSON structure in language: {language}. Please use {search_intent} to create a perfect structure."},
        ]
        )

        response_json_string = response.choices[0].message.content
        cleaned_json_string = response_json_string.strip().encode('utf-8')
        response_json = json.loads(cleaned_json_string)

        print (response_json)
        
        #response_json = json.loads(response_json_string)
        #response_json = demjson.decode(response_json_string)
        return response_json
    
    except json.JSONDecodeError:
        print("Failed to decode JSON. The response content might be empty or malformed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return {}  # Return an empty dictionary on failure

def get_search_intent(keywords, secondary_keyword, third_keyword, language):
    query = f"{keywords}, {secondary_keyword} and {third_keyword}"
    language = language
    search_intent = ""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": '''
              You are a professional SEO with more than 10 years of experience and knowledge, you are a great copywriter in SEO. '''},
            {"role": "user", "content": f"extract search intent for this main keyword: {keywords} and for these secondaries keyword: {secondary_keyword}, {third_keyword}. Please be sure to use this language: {language}"},
        ]
        )
    
    if response.choices and len(response.choices) > 0:
        search_intent = response.choices[0].message['content'].strip()
    else:
        search_intent = "Unable to extract search intent."

    print(f"Search intent is: {search_intent}")

    return search_intent


def write_section(keyword, intro, h2, h3, brief, lang, model, raw_content, json_structure, tokens_consumed, search_intent):

    if raw_content != "":
        raw_content = f"Here is the raw content to use to get inspiration: {raw_content}"

    json_structure_string = json.dumps(json_structure)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": '''
                As a skilled assistant and proficient content creator, your task involves crafting an SEO-enhanced section of a full article, with a focus on a primary keyword and guided by a brief. 
                To elevate the article's appeal and readability, integrate HTML elements such as <strong> tags for emphasis, 
                <a href='URL'> for external links, and utilize unordered lists (<ul>) with list items (<li>) to organize information effectively. Please be sure this is well formated for accents in utf-8.
                This approach not only enriches the content's presentation but also optimizes it for search engines, potentially improving its visibility and engagement with the target audience. Use <h3> if you are writing a H3 section.
                Don't repeat content used in other sections, and ensure the content is unique and engaging.
            '''},
            {"role": "user", "content": f"Main Keyword: {keyword}, Brief: {brief}, Language: {lang}. {raw_content}. Please write an SEO-optimized section of an entire article. The section title is: '{h3}' and the father category is: '{h2}'. Here's the entire article structure {json_structure_string}. Please remember the {search_intent} and create an {intro}"},
        ]
    )

    print (f"Main Keyword: {keyword}, Brief: {brief}, Language: {lang}. {raw_content}. Please write an SEO-optimized section of an entire article. The section title is: '{h3}' and the father category is: '{h2}'. Here's the entire article structure {json_structure_string} and {search_intent} and please create an {intro} and use {keyword} in the first 3 lines of article.")

    tokens_consumed += response.usage.total_tokens

    return response.choices[0].message.content



def extract_titles(json_structure, keyword, model, brief, language, raw_content, search_intent):
    search_intent = ""
    intro = ""
    tokens_consumed = 0
    print ("Starting to write the article...")
    full_article=""
    # Check if the top-level key 'subsections' exists
    if 'subsections' in json_structure:
        
        for section in json_structure['subsections']:
            # Extract H2 titles
            if 'title' in section:
                h2 = section['title']
                full_article += "<h2>" + h2 + "</h2>"
            
            # Check and extract H3 titles if they exist
            if 'subsections' in section:
                h3_titles = []
                for subsection in section['subsections']:
                    if 'title' in subsection:
                        h3_titles.append(subsection['title'])
            
            # Recursively extract H2 and H3 titles from subsections
            for h3 in h3_titles:
                print (f"Writing H3 section {h3} under H2 section {h2} in the article.")
                h3_section = write_section(keyword, intro, h2, h3, brief, language, model, raw_content, json_structure, tokens_consumed, search_intent)
                full_article += h3_section
    
    return full_article, tokens_consumed