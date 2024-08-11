import os
from tqdm import tqdm
import re
import requests
from threading import Thread

ROOT_PATH = os.path.abspath(".")

DATA_PATH = os.path.join(ROOT_PATH, 'data')

def download_csv(file_name: str, url: str, progress_bar:tqdm = None):
    response = requests.get(url)
    os.makedirs(DATA_PATH, exist_ok=True)

    file_path = os.path.join(DATA_PATH, f'{file_name}.csv')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

    if progress_bar is not None:
        progress_bar.update()

def fetch_csv_urls():
    response = requests.get("http://dados.prefeitura.sp.gov.br/pt_PT/dataset/dados-do-sp156")

    return re.findall(r'href="(.*\.csv)"', response.text)

def download_csvs(urls:list[str]):
    progress_bar = tqdm(desc="SP156 Relatories", total=len(urls))
    
    threads = []

    for index, url in enumerate(urls):
        file_name = f'file_{index+1}'
        thread = Thread(target=download_csv, args=(file_name, url, progress_bar))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    urls = fetch_csv_urls()

    download_csvs(urls)