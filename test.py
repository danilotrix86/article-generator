from nlp.openai_client import OpenAIClient
import json

keywords = "how to clean your face, daily skincare routine, face cleaning, how?"
topics_n = 5
language = "english"



###########################################################################################################################
# EXTRACT THE TOPICS AND SUBTOPICS FOR A LONG-FORM ARTICLE
###########################################################################################################################

print ("Extracting topics and subtopics for a long-form article...")
extract_topics_system = "You are a powerfull and experienced SEO and Content expert. You are specialized in extract topics and subtopics starting from keywords"
extract_topics_user = f'''
    Given a set of keywords: {keywords}, this function generates a comprehensive list of potential topics and subtopics
    for a detailed long-form article. The article aims to cover various aspects related to the keywords,
    including practical advice, technological innovations, societal impacts, and personal stories.

    The function returns a JSON structure that includes:
    - {topics_n} major topics that are essential for a thorough understanding of the given keywords.
    - A series of subtopics under each major topic, detailing specific aspects, methods, challenges, and solutions.

    The goal is to provide a broad yet detailed framework that captures the multifaceted nature of the topics,
    appealing to readers at various stages of their interest or involvement.

    Returns:
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
'''

json_structure = OpenAIClient("gpt-3.5-turbo", 0, True)
json_structure.add_to_message(extract_topics_system, "system")
json_structure.add_to_message(extract_topics_user, "user")

answer, usage = (json_structure.completions())

topics_json = json.loads(answer)

print (topics_json)


###########################################################################################################################
# EXTRACT THE SEARCH INTENT FROM THE KEYWORDS
###########################################################################################################################

