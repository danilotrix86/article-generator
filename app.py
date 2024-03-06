from utils.utils import extract_json, extract_titles


model = "gpt-4-0125-preview"
keywords = "Cosa vedere a Napoli"
secondary_keyword =" cosa visitare a Napoli"
third_keyword =" cose da non perdere a Napoli"
brief = "The style should be informative and helpful, and the tone should be friendly and engaging. Write as a Human would do, not as a robot."
search_intent = ""



raw_content='''

'''
language = "italiano"
h2_count = "4"
h3_count = "2"


# Extract the JSON structure from the API response
json_structure = extract_json(model, keywords, secondary_keyword, third_keyword, brief, language, h2_count, h3_count, raw_content, search_intent)
print(json_structure)


# CREATE THE ARTICLE

full_article, tokens_consumed = extract_titles(json_structure, keywords, model, brief, language, raw_content, search_intent)
print (full_article)

# WRITE THE ARTICLE TO A FILE
with open("article{keywords}.html", "w") as file:
     file.write(full_article)

total_cost = (tokens_consumed*20) / 1000000
print (f"Total tokens consumed: {tokens_consumed} - Total cost: ${total_cost} USD")