from bs4 import BeautifulSoup # type: ignore
import requests
from typing import List, Final
import sys
from pathlib import Path
import os
from zipfile import ZipFile

def get_zip_urls(url: str, zip_urls:List[str]=[]):
        print(f'Downloading links from {url}')
        response = requests.get(url)
        if (response.status_code==200):
            soup = BeautifulSoup(response.text, 'html.parser')
            zip_links = [link.get('href') for link in soup.find('p').find_all_next('a')]
            if (len(zip_links)>0):
                main_pages = 'http://www.gutenberg.org/robot/' + zip_links[-1]
                return get_zip_urls(main_pages, zip_urls + zip_links[:-1])

        return zip_urls


def fetch_books(zip_links: List[str], path_to_files: str):
    i:int = 0

    for zip in zip_links:
        try:
            i += 1
            download = requests.get(zip, stream=True)
            print('Downloading file no ' + str(i) + '. Progress: ' + str(round(i/len(zip_links)*100)) + '%')

            file_name: str = path_to_files + str(i) + '.zip'
            with open(file_name, 'wb') as f:
                for dl in download.iter_content():
                    f.write(dl)

            with ZipFile(file_name) as z:
                z.extractall(path_to_files)

            os.remove(file_name)

        except KeyboardInterrupt:
            exit(0)
        except:
            print(f'Could not download {zip}')

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print('Usage: python PG_Downloader.py language_code download_directory')
        print('Example: python PG_Downloader.py en books')
        exit(1)
    lang: Final[str] = sys.argv[1]
    directory: Final[str] = sys.argv[2]

    if not os.path.exists(directory):
        os.makedirs(directory)

    url: Final[str] = 'http://www.gutenberg.org/robot/harvest?&filetypes[]=txt&langs[]=' + lang

    fetch_books(get_zip_urls(url), f'./{directory}/')
