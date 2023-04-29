import os
import requests
from bs4 import BeautifulSoup

person_pages = {
    'julia_lane': 'https://dataifa.github.io/difa-project/julia_lane.html',
    'timothy_beatty': 'https://dataifa.github.io/difa-project/timothy_beatty.html',
    'jason_owen_smith': 'https://dataifa.github.io/difa-project/jason_owensmith.html',
    'ayaz_hyder': 'https://dataifa.github.io/difa-project/ayaz_hyder.html',
    'charlotte_ambrozek': 'https://dataifa.github.io/difa-project/charlotte_ambrozek.html',
    'wen_you': 'https://dataifa.github.io/difa-project/wen_you.html',
    'nichole_szembrot': 'https://dataifa.github.io/difa-project/nichole_szembrot.html',
    'mark_prell': 'https://dataifa.github.io/difa-project/mark_prell.html',
    'bruce_weinberg': 'https://dataifa.github.io/difa-project/bruce_weinberg.html',
    'matt_bombyk': 'https://dataifa.github.io/difa-project/matt_bombyk.html',
    'joe_cummins': 'https://dataifa.github.io/difa-project/joe_cummins.html',
}

static_folder = 'static'

for name, url in person_pages.items():
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.find('img')
        img_url = img_tag.get('src')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        if not img_url.startswith('http'):
            img_url="https://dataifa.github.io/difa-project/"+img_url
        img_response = requests.get(img_url, headers=headers, stream=True)

        if img_response.status_code == 200:
            img_path = os.path.join(static_folder, f'{name}.jpg')

            with open(img_path, 'wb') as img_file:
                for chunk in img_response.iter_content(chunk_size=8192):
                    img_file.write(chunk)
        else:
            print(f"Failed to download image for {name}. Status code: {img_response.status_code}")

    else:
        print(f"Failed to access page for {name}. Status code: {response.status_code}")
