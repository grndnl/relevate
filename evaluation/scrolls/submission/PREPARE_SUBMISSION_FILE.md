# SCROLLS - Prepare Submission File

A script for preparing a SCROLLS submission file.
***

### Requirements
* [Setup](https://github.com/tau-nlp/scrolls/blob/main/evaluator/README.md#setup) environment.
* [Prediction Format](https://github.com/tau-nlp/scrolls/blob/main/evaluator/README.md#prediction-format) expected by the script below.

***

Please set:
* `{dataset_name}_PREDS_FILE` to be the path to a file in the format described in [Predictions Format](#https://github.com/tau-nlp/scrolls/blob/main/evaluator/README.md#prediction-format) containing your predictions for `{dataset_name}`.
  
* `OUTPUT_DIR` to be the path you want the submission file will be saved to.

Run:

```python
python prepare_submission.py --qasper_file data/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/original
python prepare_submission.py --qasper_file data/grobid/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/grobid
python prepare_submission.py --qasper_file data/nougat/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/nougat
python prepare_submission.py --qasper_file data/pypdf/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/pypdf
python prepare_submission.py --qasper_file data/source/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/source
python prepare_submission.py --qasper_file data/our_method/generated_predictions.json --gov_report_file data/original/mock_gov_report.json --summ_screen_file data/original/mock_sfd.json --qmsum_file data/original/mock_qmsum.json --narrative_qa_file data/original/mock_nqa.json --quality_file data/original/mock_qual.json --contract_nli_file data/original/mock_cnli.json --output_dir submission/our_method
```

To verify your output file is valid, please see [Verify Submission File](https://github.com/tau-nlp/scrolls/blob/main/evaluator/VERIFY_SUBMISSION_FILE.md).

Upload the file to the [SCROLLS website](https://www.scrolls-benchmark.com) (you may need to login first).
