import pandas as pd
import json


def main():
    test_data = pd.read_json("../qmsum/test.jsonl", lines=True)

    ids = test_data['id'].to_list()
    mock_qmsum_data = {id: 'mock' for id in ids}

    with open('data/mock_qmsum.json', 'w') as f:
        json.dump(mock_qmsum_data, f)


if __name__ == "__main__":
    main()
