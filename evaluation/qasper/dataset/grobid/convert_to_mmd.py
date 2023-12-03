from pathlib import Path
import json
from tqdm import tqdm


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def save_dataset(dataset, split, out_path):
    for paper_id in tqdm(dataset, f"Saving {split} dataset"):
        out_dir = out_path / split / f"{paper_id}.mmd"
        out_dir.parent.mkdir(parents=True, exist_ok=True)
        with open(out_dir, 'w', encoding='utf-8') as f:
            f.write(dataset[paper_id])
    return


def convert_dataset(path, split, out_path):
    json_paths = get_all_files(path / split, "*.json")

    dataset = {}
    for json_path in tqdm(json_paths, desc=f"Processing {split} inputs"):
        with open(json_path, 'r') as f:
            data = json.load(f)
        paper_id = json_path.stem

        paper_text = []
        # title and authors
        paper_text.append(data['title'] + '\n')
        paper_text.append(', '.join([author['first'] + ' ' + author['last'] + '\n' for author in data['authors']]) + '\n\n')

        # abstract
        paper_text.append('Abstract\n\n' + data['abstract'] + '\n\n')

        # Main text
        prior_section = ''
        for sentence in data['pdf_parse']['body_text']:
            text = sentence['text']
            section = sentence['section']
            if section != prior_section:
                paper_text.append(f"\n{section}\n{text}")
            else:
                paper_text.append(text)
            prior_section = section

        # References
        paper_text.append('\n\nReferences\n')
        for entry in data['pdf_parse']['bib_entries']:
            paper_text.append('\n* ' + data['pdf_parse']['bib_entries'][entry]['raw_text'])

        dataset[paper_id[:10]] = " ".join(paper_text)

    save_dataset(dataset, split, out_path)
    return


if __name__ == "__main__":
    path = Path("dataset")
    out_path = Path("dataset_mmd")

    for split in ['dev', 'train', 'test']:
        convert_dataset(path, split, out_path)
