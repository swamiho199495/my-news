import requests
import os
import json
from datetime import datetime

# GitHub Secrets मधून API Key घेणे
API_KEY = os.getenv('GNEWS_API_KEY')
# मराठी बातम्यांसाठी URL
URL = f"https://gnews.io/api/v4/top-headlines?category=general&lang=mr&country=in&max=10&apikey={API_KEY}"

def download_image(image_url, file_name):
    try:
        if image_url and image_url.startswith('http'):
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # images फोल्डरमध्ये फोटो सेव्ह करणे
                with open(f"images/{file_name}", 'wb') as f:
                    f.write(response.content)
                return f"images/{file_name}"
    except Exception as e:
        print(f"फोटो डाऊनलोड करताना एरर आला: {e}")
        return None
    return None

# बातम्या मिळवा
try:
    response = requests.get(URL)
    data = response.json()

    if 'articles' in data:
        new_articles = []
        for i, article in enumerate(data['articles']):
            # प्रत्येक फोटोला वेगळे नाव देणे
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"img_{timestamp}_{i}.jpg"
            
            # फोटो डाऊनलोड करून त्याचा मार्ग (Path) मिळवणे
            local_path = download_image(article.get('image'), image_name)
            article['local_image_path'] = local_path
            new_articles.append(article)

        # जुन्या बातम्या वाचणे (Backup/Memory)
        file_path = 'news_data.json'
        old_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)

        # नवीन बातम्या जुन्या बातम्यांच्या वर जोडणे
        combined_data = new_articles + old_data
        # जास्तीत जास्त १०० बातम्या साठवणे (स्टोरेज मॅनेजमेंट)
        combined_data = combined_data[:100]

        # फाईलमध्ये सेव्ह करणे
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)
        print("यशस्वी: बातम्या आणि फोटो सेव्ह झाले!")

    else:
        print("API कडून बातम्या मिळाल्या नाहीत. कृपया API Key तपासा.")

except Exception as e:
    print(f"काहीतरी तांत्रिक अडचण आली: {e}")
