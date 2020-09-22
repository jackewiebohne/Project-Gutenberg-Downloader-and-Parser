from bs4 import BeautifulSoup
import requests

empty_lst = []
def IterateThroughGutenbergPages(start_url): #recursively iterates through all the pages & stores all the links to the zip files in a list
    try:
        print('downloading links')
        response = requests.get(start_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        zip_links = [link.get('href') for link in soup.find('p').find_all_next('a')]
        main_pages = 'http://www.gutenberg.org/robot/' + zip_links[-1]
        empty_lst.append(zip_links[:-1])
        func_call = IterateThroughGutenbergPages(main_pages)
    except:
        pass
    return


fails = []
def GutenbergZipDownloader(zip_links, counter_start:int, path_to_files:str):
    i = counter_start
    try:
        for lst in zip_links:
            for zip in lst:
                i += 1
                download = requests.get(zip, stream=True)
                print('downloading file no ' + str(i) + '. Progress: ' + str(round(i/len(zip_links), 2)) + '%')
                try:
                    with open(path_to_files + str(i) + '.zip', 'wb') as f:
                        for dl in download.iter_content(1024): # this is the max file size it's supposed to read to memory
                            f.write(dl)
                except:
                    fails.append(i)
                    continue
    except:
        print(fails)
    return fails

counter_start = 0
start_url = 'http://www.gutenberg.org/robot/harvest?&filetypes[]=txt&langs[]=de' #change ending of this string for other languages, e.g. 'en'  for English
path_to_files = './Gutenberg ebooks/'
x = IterateThroughGutenbergPages(start_url)
y = GutenbergZipDownloader(empty_lst, counter_start, path_to_files=path_to_files)
