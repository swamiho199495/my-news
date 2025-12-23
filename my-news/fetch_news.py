import requests
import os
import json
from datetime import datetime

# GitHub Secrets मधून API Key घेणे
API_KEY = os.getenv('GNEWS_API_KEY')
# मराठी बातम्यांसाठी URL (GNews API)
URL = f"https://gnews.io/api/v4/top-headlines?category=general&lang=mr&country=in&max=10&apikey={API_KEY}"

def download_image(image_url, file_name):
    try:
        if image_url and image_url.startswith('http'):
            # images फोल्डर रिपॉझिटरीच्या रूटमध्ये (बाहेर) असावे
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # फोल्डर नसेल तर तयार करणे
                if not os.path.exists('images'):
                    os.makedirs('images')
                with open(f"images/{file_name}", 'wb') as f:
                    f.write(response.content)
                return f"images/{file_name}"
    except Exception as e:
        print(f"फोटो डाऊनलोड करताना एरर: {e}")
    return None

try:
    response = requests.get(URL)
    data = response.json()

    if 'articles' in data:
        new_articles = []
        for i, article in enumerate(data['articles']):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"img_{timestamp}_{i}.jpg"
            local_path = download_image(article.get('image'), image_name)
            article['local_image_path'] = local_path
            new_articles.append(article)

        file_path = 'news_data.json'
        old_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)

        combined_data = new_articles + old_data
        combined_data = combined_data[:100] # १०० बातम्यांची मर्यादा

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)
        print("यशस्वी: बातम्या सेव्ह झाल्या!")
    else:
        print("बातम्या मिळाल्या नाहीत. API Key तपासा.")

except Exception as e:
    print(f"अडचण आली: {e}")
