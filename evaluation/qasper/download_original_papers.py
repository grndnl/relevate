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
    qasper_train = pd.read_json("dataset/qasper-train-v0.3.json", convert_axes=False).transpose()
    qasper_dev = pd.read_json("dataset/qasper-dev-v0.3.json", convert_axes=False).transpose()
    qasper_test = pd.read_json("dataset/qasper-test-v0.3.json", convert_axes=False).transpose()

    split = 'train'
    downloaded = get_all_names(split, "*.pdf")
    papers_train = qasper_train.index.to_list()
    download_papers(papers_train, split, downloaded, filetype)

    split = 'dev'
    downloaded = get_all_names(split, "*.pdf")
    papers_dev = qasper_dev.index.to_list()
    download_papers(papers_dev, split, downloaded, filetype)

    split = 'test'
    downloaded = get_all_names(split, "*.pdf")
    papers_test = qasper_test.index.to_list()
    download_papers(papers_test, split, downloaded, filetype)


if __name__ == '__main__':
    # main(filetype=['pdf'])
    main(filetype=['src'])
