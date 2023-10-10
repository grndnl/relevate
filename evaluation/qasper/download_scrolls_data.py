from datasets import load_dataset

qasper_dataset = load_dataset("tau/scrolls", "qasper")
"""
Options are: ["gov_report", "summ_screen_fd", "qmsum", "narrative_qa", "qasper", "quality", "contract_nli"]
"""

print("done")