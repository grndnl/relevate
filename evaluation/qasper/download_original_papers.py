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

def download_papers(papers, split, downloaded):
    os.makedirs(split, exist_ok=True)
    for paper in tqdm(papers, desc=f"Downloading {split} papers"):
        if paper not in downloaded:
            path = os.path.join('qasper'+split, paper+'.pdf')
            try:
                written_path, _ = urlretrieve(f"https://export.arxiv.org/pdf/{paper}.pdf", path)
            except urllib.error.URLError as e:
                print(e)
                print(paper)
            time.sleep(16)
    return


if __name__ == '__main__':
    qasper_train = pd.read_json("dataset/qasper-train-v0.3.json", convert_axes=False).transpose()
    qasper_dev = pd.read_json("dataset/qasper-dev-v0.3.json", convert_axes=False).transpose()
    qasper_test = pd.read_json("dataset/qasper-test-v0.3.json", convert_axes=False).transpose()


    split = 'train'
    downloaded = get_all_names(split, "*.pdf")
    papers_train = qasper_train.index.to_list()
    download_papers(papers_train, split, downloaded)

    split = 'dev'
    downloaded = get_all_names(split, "*.pdf")
    papers_dev = qasper_dev.index.to_list()
    download_papers(papers_dev, split, downloaded)

    split = 'test'
    downloaded = get_all_names(split, "*.pdf")
    papers_test = qasper_test.index.to_list()
    download_papers(papers_test, split, downloaded)
