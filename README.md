 Project Description
This project implements an end-to-end data platform to collect, process, and visualize news related to Iran-USA tensions. The architecture follows the Medallion model (Bronze, Silver, Gold) and utilizes a local Data Lake based on MinIO.

 Technical Architecture
Hybrid Ingestion: Supports Batch mode (scheduled scraping) and Streaming mode (each article is a unique JSON event).

Data Lake (MinIO): Distributed storage for raw and refined data.

Processing (ETL): HTML cleaning, text normalization, and automatic language detection (FR/EN).

Data Warehouse (Gold): Aggregation of media trends and dominant keyword analysis.

Visualization: Interactive dashboard developed with Streamlit.

Tech Stack
Language: Python 3.x

Collection: BeautifulSoup4, Requests

Storage: MinIO (S3 compatible via Boto3)

Orchestration: Automated pipeline logic (ready for Apache Airflow)

Dashboard: Streamlit
