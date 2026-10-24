Overview
Instamart Customer Intelligence & Support Copilot — Capstone Project

Reproduce
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate_data.py
python src\part_a\clean_data.py
python src\part_a\build_db.py
python src\part_a\validate.py
python src\part_a\run_sql.py
python src\part_b\rfm.py
python src\part_b\segmentation.py
python src\part_b\lapse_prediction.py

Part A
Audit Results
Orders Raw: 13084
Exact Duplicates: 119
Pending Rows: 656
Distinct Order IDs: 12309
Customer Cleaning
Female: 610
Male: 560
Unknown: 30
Missing Ages: 0
Age Range: 18-60
Order Cleaning
Rows: 12309
Completed: 11110
Cancelled: 1199
Revenue: INR 2,998,668.80
Validation
ALL CHECKPOINTS PASSED

Part B
RFM
Customers: 1175
Recency Median: 19
Recency Min: 0
Recency Max: 180
Frequency Mean: 9.46
Frequency Max: 33
Monetary Mean: INR 2552.06
Monetary Max: INR 14766.55
SegmentsSize:
436
138
419
182
PCA
PC1: 0.63427875
PC2: 0.21803762

Part C
Work in progress

Part D
Work in progress

Limitations and Next Steps
Complete lapse prediction model
Build ticket triage system
Build RAG assistant
Build refund agent