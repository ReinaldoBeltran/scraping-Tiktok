from flask import Flask, render_template, request
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import requests
import webbrowser
import random

app = Flask(__name__)

def downloadVideo(link, id, output_path):
    cookies = {
        '_gid': 'GA1.2.1911979192.1699627041',
        '_gat_UA-3524196-6': '1',
        '_ga': 'GA1.1.1839308849.1697408314',
        '_ga_ZSF3D6YSLC': 'GS1.1.1699709851.11.1.1699711281.0.0.0',
    }
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'es-US,es-419;q=0.9,es;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gid=GA1.2.1911979192.1699627041; _gat_UA-3524196-6=1; _ga=GA1.1.1839308849.1697408314; _ga_ZSF3D6YSLC=GS1.1.1699709851.11.1.1699711281.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'UnltVDM1',
    }

    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    downloadLink = downloadSoup.a["href"]

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    filename = f"{id}.mp4"
    output_file = os.path.join(output_path, filename)

    with open(output_file, "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                return True
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    cuenta = request.form['cuenta']
    ruta_destino = request.form['ruta_destino']
    nombre_carpeta = request.form['nombre_carpeta']
    tiempo_espera = int(request.form['tiempo_espera'])

    output_path = os.path.join(ruta_destino, nombre_carpeta)
    os.makedirs(output_path, exist_ok=True)

    driver = webdriver.Chrome()
    driver.get(cuenta)
    time.sleep(tiempo_espera)

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    videos = soup.find_all("div", {"class": "tiktok-16ou6xi-DivTagCardDesc"})

    count = 0
    for index, video in enumerate(videos):
        url = video.a["href"]
        result = None
        tries = 0
        while result is None and tries < 10:
            try:
                result = downloadVideo(url, count, output_path)
                tries += 1
            except:
                time.sleep(30)
                pass
            time.sleep(10)
        count += 1

    driver.quit()

    return "Videos descargados correctamente."

if __name__ == '__main__':
    port = random.randint(5001, 9999)  # Genera un puerto aleatorio entre 5001 y 9999
    url = f'http://127.0.0.1:{port}'  # URL local con el puerto aleatorio

    # Abre automáticamente la URL en el navegador predeterminado
    webbrowser.open(url)

    app.run(port=port)