import requests
from bs4 import BeautifulSoup
import json
import boto3
from datetime import datetime

s3 = boto3.client('s3', endpoint_url='http://localhost:9000', 
                  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')

SOURCES = {
    "Al Jazeera": "https://www.aljazeera.com/tag/iran-us-tensions/",
    "Hespress": "https://fr.hespress.com/monde",
    "BBC News": "https://www.bbc.com/news/world/middle_east",
    "Reuters": "https://www.reuters.com/world/middle-east/"
}

def collecter_et_stocker():
    headers = {'User-Agent': 'Mozilla/5.0'}
    for name, url in SOURCES.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            tags = soup.find_all(['h2', 'h3'], limit=5)
            for tag in tags:
                data = {
                    "titre": tag.text.strip(),
                    "source": name,
                    "url": url,
                    "date_collecte": datetime.now().isoformat(),
                    "html_content": str(tag.parent)
                }
                file_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                # Envoi du dictionnaire JSON
                s3.put_object(Bucket='bronze', Key=f"{name.replace(' ', '_')}_{file_id}.json", Body=json.dumps(data))
            print(f"✅ Ingestion Bronze réussie : {name}")
        except Exception as e:
            print(f"❌ Erreur sur {name} : {e}")

if __name__ == "__main__":
    collecter_et_stocker()