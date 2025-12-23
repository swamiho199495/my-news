import requests
import os
import json

API_KEY = os.getenv('GNEWS_API_KEY')

# कॅटेगरी आणि सर्च कीवर्ड्स
SEARCH_TOPICS = {
    'general': 'https://gnews.io/api/v4/top-headlines?category=general&lang=mr&country=in&max=10',
    'market': 'https://gnews.io/api/v4/search?q="शेअर मार्केट" OR "गुंतवणूक" OR "BSE" OR "NSE"&lang=mr&country=in&max=10',
    'it_tech': 'https://gnews.io/api/v4/search?q="तंत्रज्ञान" OR "आयटी" OR "AI" OR "स्मार्टफोन"&lang=mr&country=in&max=10',
    'sports': 'https://gnews.io/api/v4/top-headlines?category=sports&lang=mr&country=in&max=10',
    'entertainment': 'https://gnews.io/api/v4/top-headlines?category=entertainment&lang=mr&country=in&max=10'
}

def fetch_news(url):
    try:
        full_url = f"{url}&apikey={API_KEY}"
        response = requests.get(full_url)
        return response.json().get('articles', [])
    except:
        return []

all_news = {}
for topic, url in SEARCH_TOPICS.items():
    print(f"Fetching {topic}...")
    all_news[topic] = fetch_news(url)

with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_news, f, indent=4, ensure_ascii=False)
