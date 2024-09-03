import re
import csv
import glob
import requests
import unicodedata
from tqdm import tqdm
from threading import Thread
from os import makedirs, path

ROOT_PATH = path.abspath(path.dirname(path.dirname(__file__)))

DATA_PATH = path.join(ROOT_PATH, 'data')
RAW_DATA_PATH = path.join(DATA_PATH, 'raw')
FINAL_DATA_PATH = path.join(DATA_PATH, 'final')
ALL_DATA_FILE_PATH = path.join(FINAL_DATA_PATH, 'all_data.csv')

COLUMNS_TO_KEEP = [
"data de abertura",
"canal",
"orgao",
"tema",
"assunto",
"servico",
"bairro",
"cep",
"distrito",
"latitude",
"logradouro",
"longitude",
"quadra",
"numero",
]


makedirs(DATA_PATH, exist_ok=True)
makedirs(RAW_DATA_PATH, exist_ok=True)
makedirs(FINAL_DATA_PATH, exist_ok=True)

def download_csv(file_name: str, url: str, progress_bar:tqdm = None):
    response = requests.get(url)

    file_path = path.join(RAW_DATA_PATH, f'{file_name}.csv')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

    if progress_bar is not None:
        progress_bar.update()

def fetch_csv_urls():
    response = requests.get("http://dados.prefeitura.sp.gov.br/pt_PT/dataset/dados-do-sp156")

    return re.findall(r'href="(.*\.csv)"', response.text)

def download_csvs_from_sp156():
    urls = fetch_csv_urls()
    
    progress_bar = tqdm(desc="Downloading SP156 Relatories", total=len(urls))
    
    threads = []

    for index, url in enumerate(urls):
        file_name = f'file_{index+1}'
        thread = Thread(target=download_csv, args=(file_name, url, progress_bar))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def get_downloaded_csvs():
    path_name = path.join(RAW_DATA_PATH, '*.csv')

    files = glob.glob(path_name)

    return sorted(files, key=lambda file: int(re.findall('(\d+)', file)[0]))

def normalize_text(text:str):
   return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower().strip()

def open_csv_writer(filepath:str):
    file_descriptor = open(filepath, '+w')

    return csv.writer(file_descriptor, delimiter=';')

def open_csv_reader(filepath:str):
    file_descriptor = open(filepath, 'r')

    return csv.reader(file_descriptor, delimiter=';')

def concat_downloaded_csvs_to_single_file():
    downloaded_csvs = get_downloaded_csvs()

    valid_csvs = downloaded_csvs[:-6] # remove csvs from 2014 to 2012

    all_data_csv_writer = open_csv_writer(ALL_DATA_FILE_PATH)

    all_data_csv_writer.writerow(COLUMNS_TO_KEEP)
    
    for csv_file in tqdm(valid_csvs[:-6], desc="Concatenating rows to a single file"):
        csv_reader = open_csv_reader(csv_file)

        headers = next(csv_reader)

        normalized_headers = list(map(lambda head: normalize_text(head), headers))

        indexes = list(map(lambda column: None if column not in normalized_headers else normalized_headers.index(column), COLUMNS_TO_KEEP))

        for row in csv_reader:
            mapped_row = map(lambda index:None if index is None else row[index], indexes)

            all_data_csv_writer.writerow(list(mapped_row))

def separate_all_data_to_themes():
    all_data_csv = open_csv_reader(ALL_DATA_FILE_PATH)

    header = next(all_data_csv)

    theme_index = header.index('tema')
    print(theme_index)
    file_map = dict()

    for row in tqdm(all_data_csv, desc="Separating rows to multiple files"):
        print(row, theme_index)
        
        theme = row[theme_index].replace('/', '').replace('\\', '')

        if not file_map.get(theme):
            theme_file = path.join(FINAL_DATA_PATH, f'{theme}.csv')

            file_map[theme] = open_csv_writer(theme_file)
            file_map[theme].writerow(header)

        file_map[theme].writerow(row)


if __name__ == "__main__":
    download_csvs_from_sp156()

    concat_downloaded_csvs_to_single_file()

    separate_all_data_to_themes()