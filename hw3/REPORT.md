Data Quality Summary

We analyzed page_blocks_dirty.csv using mechanical gawk checks (S1–S5) and Python-based checks (A–G) to identify structural and data quality issues in the dataset.

Structural Integrity (S1–S5)
	•	Ragged Rows (S1): All records have a consistent number of fields and no ragged rows were found.
	•	Missing Values (S2): Missing values appear in 23 rows, specifically in the MEAN_TR and P_AND columns (rows: 24, 172, 180, 977, 1007, 1047, 1081, 1227, 1558, 1643, 1967, 2009, 2303, 2534, 2953, 2983, 3065, 3368, 3406, 3886, 3980, 5357, 5417).
	•	Constant Columns (S3): The DATASET_ID column is constant across all rows and does not provide meaningful variation.
	•	Invalid Class Labels (S4): A total of 5 rows contain class labels outside the allowed range {1–5} (rows: 4, 987, 1222, 1289, 4831).
	•	Duplicate Rows (S5): A total of 76 duplicate records were identified, indicating redundancy in the dataset.

Data Quality Issues (A–G)
	•	Identical Feature Groups (A): 1 pair of features are identical: LENGHT and WIDTH.
	•	Correlated Feature Pairs (B): 2 pairs of features show high correlation: LENGHT,WIDTH and BLACKPIX,BLACKAND.
	•	Outlier Features (C): 9 features contain outlier values: HEIGHT, LENGHT, WIDTH, AREA, ECCEN, P_BLACK, BLACKPIX, BLACKAND, WB_TRANS.
	•	Conflicting Features (D): 7 features have conflicting values: AREA, BLACKAND, BLACKPIX, HEIGHT, LENGHT, P_AND, P_BLACK.
	•	Implausible Features (E): 3 features contain implausible values: HEIGHT, P_AND, P_BLACK.
	•	Outlier Cases (G): 609 rows contain outlier values across various features.

Overall Assessment

The dataset exhibits significant data quality issues across multiple dimensions. Structural problems include 23 missing values, 76 duplicate records, 5 invalid class labels, and a non-informative constant feature (DATASET_ID). 

More concerning are the data quality issues: identical features (LENGHT and WIDTH), high correlations suggesting redundancy, widespread outliers affecting 9 features and 609 cases (11% of the dataset), conflicting values in 7 features, and implausible values in 3 features. These issues significantly impact data reliability and require careful cleaning before modeling or analysis.
