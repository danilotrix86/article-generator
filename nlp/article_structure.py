from nlp.openai_client import OpenAIClient
from config import config

def generate_article_structure(list_of_keywords, brief, section_n):
    aiclient = OpenAIClient(config.OPENAI_LLM_BEST_MODEL, 0, True)

    extract_topics_system = f'''
        You are a powerfull and experienced SEO and Content expert. You are specialized in creating the structure of a article starting from a list of keywords and the article brief.
        You should always returns a JSON structure that includes:
        - {section_n} major topics that are essential for a thorough understanding of the given keywords.
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
    
    keywords_str = ', '.join(str(keyword) if not isinstance(keyword, str) else keyword for keyword in list_of_keywords)
    list_of_keywords_str_and_brief = keywords_str + brief

    aiclient.add_to_message(extract_topics_system, 'system')
    aiclient.add_to_message(list_of_keywords_str_and_brief, 'user')

    return aiclient.completions()

def validate_article_structure(article_structure):
    aiclient = OpenAIClient(config.OPENAI_LLM_BEST_MODEL, 0, True)

    validate_structure_system = f'''
        You are a helpful assistant with the job of validating the structure of a article structure.
        The correct structure you should return looks like this JSON structure:
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
        Obviously, replace "the topic" and "the subtopic" with the actual topics and subtopics.
        Any other structure is not valid. If you find an invalid structure, you should return the correct structure.
        If the structure is correct, you should return "ok".
    '''

    #coonvert the article_structure to a string
    article_structure_str = str(article_structure)

    aiclient.add_to_message(validate_structure_system, 'system')
    aiclient.add_to_message(article_structure_str, 'user')

    return aiclient.completions()