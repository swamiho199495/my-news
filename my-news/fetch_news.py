import requests
import os
import json

API_KEY = os.getenv('GNEWS_API_KEY')
# आपण या ४ मुख्य कॅटेगरी घेत आहोत
CATEGORIES = ['general', 'technology', 'sports', 'entertainment', 'business']

def fetch_category_news(category):
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=mr&country=in&max=12&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('articles', [])
    except:
        return []

all_news = {}
for cat in CATEGORIES:
    print(f"Fetching {cat} news...")
    all_news[cat] = fetch_category_news(cat)

with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_news, f, indent=4, ensure_ascii=False)
