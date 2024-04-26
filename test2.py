from nlp.openai_client import OpenAIClient
import json
from keyword_research.keyword_research import keyword_research, better_keyword_research
from nlp.article_structure import generate_article_structure, validate_article_structure

keyword = "cosa vedere a Napoli"
language = "italian"
location = "Italy"
brief = "The style should be informative and helpful, and the tone should be friendly and engaging. Write as a Human would do, not as a robot."
section_n = 3


list_of_keywords = keyword_research(keyword, language, location)

list_of_working_keywords = better_keyword_research(list_of_keywords, keyword)


#article_structure = generate_article_structure(list_of_keywords, brief, section_n)

#article_structure_validated = validate_article_structure(article_structure)

print (list_of_working_keywords)

#print (article_structure_validated)
        
