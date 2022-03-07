import requests
from pyrnalist import report
import os
from appdata import AppDataPaths

DATA_GOV_PL_BASE_URL = 'https://api.dane.gov.pl/1.4/datasets/{}?lang=pl'


def download_data_gov_pl_dataset(temp_path, resource, resources_id):
    main_url = DATA_GOV_PL_BASE_URL.format(resource)
    report.verbose(f'Fetching url={main_url}...')
    r = requests.get(main_url)
    data = r.json()
    related_url = data['data']['relationships']['resources']['links']['related']
    report.verbose(f'Fetching url={related_url}...')
    r = requests.get(related_url)
    data = r.json()
    resources_data = data['data']
    filtered_resources = [r for r in resources_data if int(r['id']) in resources_id]
    filtered_csv_links = [
        {'id': r['id'], 'url': r['attributes']['csv_download_url'], 'size': r['attributes']['csv_file_size']} for r in
        filtered_resources]
    chunk_size = 4096
    files = {}
    for csv in filtered_csv_links:
        size = csv['size']
        url = csv['url']
        steps = int(size / chunk_size)
        id = csv['id']
        file_name = os.path.join(temp_path.app_data_path, f'{id}.csv')
        if not os.path.exists(file_name):
            tick = report.progress(steps)
            report.verbose(f'{file_name} not found, downloading...')
            with open(file_name, "wb") as f:
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        tick()
            tick.stop()
            report.verbose(f'Downloaded url={url}')
        report.verbose(f'Using id={id} file={file_name}')
        files[int(id)] = file_name
    return files


male_first_names_id = 36409
male_middle_names_id = 36413
female_first_names_id = 36410
female_middle_names_id = 36414


def download_first_names(temp_path):
    first_names = download_data_gov_pl_dataset(temp_path, '1501,lista-imion-wystepujacych-w-rejestrze-pesel',
                                               [male_first_names_id, male_middle_names_id, female_first_names_id,
                                                female_middle_names_id])
    return first_names


female_last_names_id = 36406
male_last_names_id = 36405


def download_last_names(temp_path):
    last_names = download_data_gov_pl_dataset(temp_path, '568,nazwiska-wystepujace-w-rejestrze-pesel',
                                              [male_last_names_id, female_last_names_id])
    return last_names


def get_datasets():
    temp_path = AppDataPaths('salamlab-testing')
    temp_path.setup()
    datasets = {'last_names': download_last_names(temp_path), 'first_names': download_first_names(temp_path)}
    return datasets
