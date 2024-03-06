from nlp.openai_client import OpenAIClient


# Find topics starting from the keywords
keywords = "Cosa vedere a Marina di Ragusa, Marina di Ragusa, Ragusa mare"
topics_n = 5
language = "italiano"
prompt = f'''
Given the keywords {keywords}, generate a comprehensive list of potential topics and subtopics for a detailed long-form article. 
The article aims to cover various aspects of {keywords}, including practical advice, technological innovations, societal impacts, and personal stories. 
Please include:
- An overarching theme or angle for the article that ties all topics together.
- {topics_n} Major topics that are essential for understanding {keywords}.
- Subtopics under each major topic that delve into specific details, methods, challenges, and solutions.
- Questions that the article should aim to answer for readers interested in {keywords}.
- Any relevant trends, statistics, or case studies that could be included to support the content.
- The goal is to provide a broad yet detailed framework that covers the multifaceted nature of {keywords}, appealing to readers at different stages of their interest or involvement.
Return a json structure like this:

{{
    title,
    topic,
        subtopic,
        subtopic,
        subtopic,
    topic,
        subtopic,
        subtopic,
        subtopic,
    topic,
        subtopic,
        subtopic,
        subtopic,
    questions_to_answer,
    relevant_trends
}}

IMPORTANT: The json structure should be written using the language: {language}*

'''

client = OpenAIClient("gpt-3.5-turbo", 0, True)
client.add_to_message(prompt, "user")


answer, tokens = (client.completions())

print (answer)
print (tokens.prompt_tokens, tokens.total_tokens)