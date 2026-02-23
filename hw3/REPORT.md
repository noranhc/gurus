Data Quality Summary

We analyzed page_blocks_dirty.csv using mechanical gawk checks (S1–S5) to identify structural issues in the dataset.

Structural Integrity (S1–S5)
	•	Ragged Rows (S1): All records have a consistent number of fields and no ragged rows were found.
	•	Missing Values (S2): Missing values (?) appear in multiple rows, particularly in the MEAN_TR and P_AND columns.
	•	Constant Columns (S3): The DATASET_ID column is constant across all rows and does not provide meaningful variation.
	•	Invalid Class Labels (S4): A total of 4 rows contain class labels outside the allowed range {1–5}.
	•	Duplicate Rows (S5): A total of 76 duplicate records were identified, indicating redundancy in the dataset.

Overall Assessment

From a structural standpoint, the dataset is mostly well-formed, but it contains several issues that should be addressed before further analysis. These include missing values, duplicate records, a non-informative feature (DATASET_ID), and a small number of invalid class labels.

Further analysis in later stages will focus on deeper integrity and plausibility checks.
