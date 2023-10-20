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


def download_papers(papers, split, downloaded, filetypes):
    for filetype in filetypes:
        for paper in tqdm(papers, desc=f"Downloading {split} papers"):
            if paper not in downloaded:
                if filetype == 'pdf':
                    path = Path('dataset', split, paper + '.pdf')
                    os.makedirs(path.parent, exist_ok=True)
                elif filetype == 'src':
                    path = Path('dataset', 'source', split, paper + '.tar.gz')
                    os.makedirs(path.parent, exist_ok=True)
                else:
                    raise f"Filetype not supported: {filetype}"
                try:
                    if filetype == 'pdf':
                        written_path, _ = urlretrieve(f"https://export.arxiv.org/pdf/{paper}.pdf", path)
                    elif filetype == 'src':
                        written_path, _ = urlretrieve(f"https://export.arxiv.org/src/{paper}", path)
                except urllib.error.URLError as e:
                    print(e)
                    print(paper)
                time.sleep(16)
    return


def main(filetype):
    for split in ['train', 'dev', 'test']:
        qasper_papers = pd.read_json(f"dataset/qasper-{split}-v0.3.json", convert_axes=False).transpose()
        if filetype == 'pdf':
            downloaded = get_all_names(split, "*.pdf")
        elif filetype == 'src':
            downloaded = get_all_names('src' + split, "*")
        else:
            raise f"Filetype not supported: {filetype}"
        papers = qasper_papers.index.to_list()
        download_papers(papers, split, downloaded, filetype)


if __name__ == '__main__':
    # main(filetype=['pdf'])
    main(filetype=['src'])
