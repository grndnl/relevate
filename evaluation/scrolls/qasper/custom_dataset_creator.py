import os
import pandas as pd
from pathlib import Path
import json
from tqdm import tqdm


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def read_custom_dataset(path, split, custom_dataset_name):
    if custom_dataset_name == "scrolls_qasper_grobid":
        json_paths = get_all_files(path / split, "*.json")

        dataset = {}
        for json_path in json_paths:
            with open(json_path, 'r') as f:
                data = json.load(f)
            paper_id = json_path.stem

            paper_text = []
            prior_section = ''
            for sentence in data['pdf_parse']['body_text']:
                text = sentence['text']
                section = sentence['section']
                if section != prior_section:
                    paper_text.append(f"\n{section}\n{text}")
                else:
                    paper_text.append(text)
                prior_section = section

            dataset[paper_id[:10]] = " ".join(paper_text)
    elif custom_dataset_name == "scrolls_qasper_source":
        raise Exception(f"Custom dataset not yet supported: {custom_dataset_name}")
    else:
        raise Exception(f"Custom dataset not supported: {custom_dataset_name}")

    return dataset


def main(custom_dataset_path, custom_dataset_name):
    for split in tqdm(['dev', 'train', 'test']):
        if split == 'dev':
            scrolls_split = 'validation'
        else:
            scrolls_split = split

        # Load custom dataset
        custom_dataset = read_custom_dataset(custom_dataset_path, split, custom_dataset_name)

        # Load scrolls qasper data
        scrolls_qasper = pd.read_json(f"{scrolls_split}.jsonl", lines=True)
        print(f"Length of {scrolls_split} original dataset: {len(scrolls_qasper)}")

        # Erase the input column after the first '\n\n'
        scrolls_qasper['input'] = scrolls_qasper['input'].apply(lambda row: row.split("\n\n")[0])

        # Load qasper data
        qasper = pd.read_json(f"../../qasper/dataset/original/qasper-{split}-v0.3.json", convert_axes=False).transpose()

        # Map qasper question id to paper id
        qas = []
        for index, row in qasper.iterrows():
            for qa in row['qas']:
                qas.append([index, qa])

        question2paper = {qa[1]['question_id']: qa[0] for qa in qas}

        # for each line in scrolls/qasper:
        for index, row in scrolls_qasper.iterrows():
            # search with the id (question id) and find the paper
            paper_id = question2paper[row['id']]

            # Load the paper text
            try:
                text = custom_dataset[paper_id]
            except KeyError:
                print(f"Paper {paper_id} not found in custom dataset")
                continue

            # Append the paper text (including section names) to the input column of the new scrolls/qasper dataframe
            scrolls_qasper.loc[index, 'input'] = scrolls_qasper.loc[index, 'input'] + '\n' + text

        # save the new dataframe
        dest = Path(f"../../{custom_dataset_name}/{scrolls_split}.jsonl")
        os.makedirs(dest.parent, exist_ok=True)
        scrolls_qasper.to_json(dest, orient='records', lines=True)

        print(f"Length of {custom_dataset_name} {scrolls_split} dataset: {len(custom_dataset)}")

    return


if __name__ == '__main__':
    custom_dataset_path = Path("../../qasper_grobid/dataset")
    custom_dataset_name = 'scrolls_qasper_grobid'

    # custom_dataset_path = Path("../../qasper/ground_truth_mmd")
    # custom_dataset_name = 'scrolls_qasper_source'

    main(custom_dataset_path, custom_dataset_name)
