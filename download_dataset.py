import os
import re
import requests
from threading import Thread

def download_csv(file_name: str, url: str):
    response = requests.get(url)
    os.makedirs('./data', exist_ok=True)
    file_path = f'./data/{file_name}.csv'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

response = requests.get("http://dados.prefeitura.sp.gov.br/pt_PT/dataset/dados-do-sp156")

urls = re.findall(r'href="(.*\.csv)"', response.text)

threads = []
for index, url in enumerate(urls):
    file_name = f'file_{index+1}'
    thread = Thread(target=download_csv, args=(file_name, url))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("All files have been downloaded.")

