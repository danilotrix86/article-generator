from openai import OpenAI
from config import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

response = client.images.generate(
  model="dall-e-3",
  prompt="sentiment analysis in python, high resolution, cartoon style image",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print (image_url)