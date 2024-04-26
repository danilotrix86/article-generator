from nlp.openai_client import OpenAIClient
import json

keywords = "Building a Smart Home System with Tessel 2"
topic = "Dive into how to use Tessel 2 as the brain of a smart home system. This article can cover integrating various sensors and modules, such as motion detectors, light sensors, and smart outlets, to create a network of IoT devices. Discuss how to use Tessel 2 to control these devices, collect data, and make smart decisions based on environmental inputs. Include examples of setting up automations, like adjusting lights based on the time of day or weather conditions, to illustrate the practical applications of Tessel 2 in home automation."
topics_n = 3
language = "english"
brief = "The style should be informative and helpful, and the tone should be friendly and engaging. Write as a Human would do, not as a robot."
search_intent = "Informative"
raw_content='''

'''
input_cost = 10
output_cost = 30


###########################################################################################################################
# EXTRACT THE TOPICS AND SUBTOPICS FOR A LONG-FORM ARTICLE
###########################################################################################################################

print ("Extracting topics and subtopics for a long-form article...")
extract_topics_system = "You are a powerfull and experienced SEO and Content expert. You are specialized in extract topics and subtopics starting from keywords"
extract_topics_user = f'''
    I give you a set of keywords: {keywords} and topic: {topic}. Generates a comprehensive list of potential topics and subtopics
    for a detailed long-form article. The article aims to cover various aspects related to the keywords,
    including practical advice, technological innovations, societal impacts, and personal stories.

    You should always returns a JSON structure that includes:
    - {topics_n} major topics that are essential for a thorough understanding of the given keywords.
    - A series of subtopics under each major topic, detailing specific aspects, methods, challenges, and solutions.

    The goal is to provide a broad yet detailed framework that captures the multifaceted nature of the topics,
    appealing to readers at various stages of their interest or involvement.

    Returns*:
    - A JSON structure with the specified number of topics and various subtopics for each, structured as follows:

    {{
        "topic": "the topic",
            "subtopic": "the subtopic",
            "subtopic": "the subtopic",
            "subtopic": "the subtopic",
        "topic": "the topic",
            "subtopic": "the subtopic",
            "subtopic": "the subtopic",
            "subtopic": "the subtopic",
        ...
    }}

    *Note: Returns A JSON

'''

json_structure = OpenAIClient("gpt-4-0125-preview", 0, True)
json_structure.add_to_message(extract_topics_system, "system")
json_structure.add_to_message(extract_topics_user, "user")

answer_json_structure, usage_json_structure = (json_structure.completions())

topics_json = json.loads(answer_json_structure)

print (topics_json)


###########################################################################################################################
# WRITING THE SINGLE SECTIONS OF THE ARTICLE
###########################################################################################################################

print ("Writing the single sections of the article...")



final_article = ""
total_token_input = 0
total_token_output = 0


write_article = OpenAIClient("gpt-4-0125-preview", 0.7, False, 1000) #gpt-4-0125-preview
write_article_system_prompt = '''
    As a skilled assistant and proficient content creator, your task involves crafting an SEO-enhanced section of a full article, with a focus on keywords and guided by a brief. 
    To elevate the article's appeal and readability, integrate HTML elements such as <strong> tags for emphasis, 
    <a href='URL'> for external links, and utilize, if makes sense, unordered lists (<ul>) with list items (<li>) to organize information effectively. Don't use other tags, like html, body, head, footer etc. Please be sure this is well formated using utf-8.
    This approach not only enriches the content's presentation but also optimizes it for search engines, potentially improving its visibility and engagement with the target audience. Always Use <h3> for the subtopic.
    Don't repeat content used in other sections.
'''
write_article.add_to_message(write_article_system_prompt, "system")
write_article.add_to_message(raw_content, "system")



# Extract the topics and subtopics
# Iterate through each topic and print its subtopics
for topic in topics_json["topics"]:
    topic_name = topic['topic']
    final_article += "<h2>" +topic_name+ "</h2>"
    for subtopic in topic["subtopics"]:
        
        print(f"Writing the subtopic {subtopic} under the topic {topic_name}...")
        write_article_user_prompt = f'''
                Main Keyword: {keywords}, Brief: {brief}, Language: {language}.
                Please write an SEO-optimized section of an entire article. 
                The section title is: '{subtopic}' and the father category is: '{topic_name}'. 
                Here's the entire article structure {answer_json_structure}. The search intent is: {search_intent}.
        '''
        write_article.add_to_message(write_article_user_prompt, "user")
        answer, usage = (write_article.completions())
        write_article.add_to_message(answer, "assistant")
        print (f"section {subtopic} under the topic {topic_name} is written....")
        final_article += answer
        print (usage)
        total_token_input += usage.prompt_tokens
        total_token_output += usage.completion_tokens
        print()  # Print a newline for better readability between topics


print()
print ("The article is completed.")

# WRITE THE ARTICLE TO A FILE
with open(f"article_{keywords}.html", "w") as file:
    file.write(final_article)
print (final_article)


cost_input = (total_token_input * input_cost) / 1000000
cost_output = (total_token_output * output_cost) / 1000000
total_cost = cost_input + cost_output
print (f"Total cost: ${cost_input} USD")