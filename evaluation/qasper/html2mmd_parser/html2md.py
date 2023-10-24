"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
import argparse
import os
import time
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup
from tqdm import tqdm
import htmlmin

# pip install nougat-ocr
from nougat.dataset.parser.latexml_parser import parse_latexml, _clean_html_whitespace
from nougat.dataset.parser.markdown import format_document


def check_file_path(paths: List[Path], wdir: Optional[Path] = None) -> List[str]:
    """
    Checks if the given file paths exist.

    Args:
        paths: A list of file paths.
        wdir: The working directory. If None, the current working directory is used.

    Returns:
        A list of file paths that exist.
    """
    files = []
    for path in paths:
        if type(path) == str:
            if path == "":
                continue
            path = Path(path)
        pathsi = [path] if wdir is None else [path, wdir / path]
        for p in pathsi:
            if p.exists():
                files.append((p.resolve()))
            elif "*" in path.name:
                files.extend([(pi.resolve()) for pi in p.parent.glob(p.name)])
    return list(set(files))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--html", type=Path, nargs="+", help="HTML file", required=True)
    # parser.add_argument("--out", type=Path, help="Output file", required=True)
    args = parser.parse_args()

    # Get all files from dir
    # file_paths = [f for f in Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset\html\train").glob("*.html")]
    file_paths = [f for f in Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset\html\dev").glob("*.html")]
    # file_paths = [f for f in Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset\html\test").glob("*.html")]
    args.html = file_paths

    args.html = check_file_path(args.html)
    # args.out = Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset/ground_truth_mmd/train")
    args.out = Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset/ground_truth_mmd/dev")
    # args.out = Path(r"C:\Users\grandid\source\repos\relevate\evaluation\qasper\dataset/ground_truth_mmd/test")

    success_count = 0
    os.makedirs(args.out, exist_ok=True)

    for f in tqdm(args.html):
        html = BeautifulSoup(
            htmlmin.minify(
                open(f, "r", encoding="utf-8").read().replace("\xa0", " "),
                remove_all_empty_space=1,
            ),
            features="html.parser",
        )
        try:
            doc = parse_latexml(html)
        except ValueError as e:
            print(e)
            continue
        if doc is None:
            continue
        out, fig = format_document(doc, keep_refs=True)
        outp = (args.out if args.out.is_dir() else args.out.parent) / (f.stem + ".mmd")
        with open(outp, "w", encoding="utf-8") as f:
            f.write(out)
        success_count += 1

    print(f"Success rate: {success_count / len(args.html)}")
    print(f"Success rate: {success_count} / {len(args.html)}")
