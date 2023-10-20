import os
import urllib.error
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from urllib.request import urlretrieve
import time


def get_all_names(directory, pattern):
    files = [f for f in Path(directory).glob(pattern)]
    return [address.stem[:10] for address in files]


def download_papers(papers, split, downloaded, filetype):
    for paper in tqdm(papers, desc=f"Downloading {split} papers as {filetype}"):
        if paper not in downloaded:
            if filetype == 'pdf':
                path = Path('dataset', split, paper + '.pdf')
                os.makedirs(path.parent, exist_ok=True)
            elif filetype == 'src':
                path = Path('dataset', 'source_zip', split, paper + '.tar.gz')
                os.makedirs(path.parent, exist_ok=True)
            elif filetype == 'html':
                path = Path('dataset', 'html', split, paper + '.html')
                os.makedirs(path.parent, exist_ok=True)
            else:
                raise Exception(f"Filetype not supported: {filetype}")
            try:
                if filetype == 'pdf':
                    written_path, _ = urlretrieve(f"https://export.arxiv.org/pdf/{paper}.pdf", path)
                elif filetype == 'src':
                    written_path, _ = urlretrieve(f"https://export.arxiv.org/src/{paper}", path)
                elif filetype == 'html':
                    written_path, _ = urlretrieve(f"https://ar5iv.labs.arxiv.org/html/{paper}", path)
            except urllib.error.URLError as e:
                print(e)
                print(paper)
            time.sleep(16)
    return


def main(filetypes):
    for filetype in filetypes:
        for split in ['train', 'dev', 'test']:
            qasper_papers = pd.read_json(f"dataset/processed_original/qasper-{split}-v0.3.json", convert_axes=False).transpose()
            if filetype == 'pdf':
                downloaded = get_all_names('pdf/' + split, "*.pdf")
            elif filetype == 'src':
                downloaded = get_all_names('source_zip/' + split, "*")
            elif filetype == 'html':
                downloaded = get_all_names('html/' + split, "*")
            else:
                raise Exception(f"Filetype not supported: {filetype}")
            papers = qasper_papers.index.to_list()
            download_papers(papers, split, downloaded, filetype)


if __name__ == '__main__':
    # main(['pdf'])
    # main(['src'])
    main(['html'])
