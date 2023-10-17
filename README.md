# Airflow-Stock-ETL
![Apache Airflow](https://github.com/ikramel-hajri/Airflow-Stock-ETL/assets/102763775/afa7e0ed-8926-4842-85d6-8fe1f1a7e7bb)

## Overview
This project focuses on the extraction, preprocessing, and automated data management of IBM stock data using various technologies, including Apache Airflow and Google Drive. It offers insights into stock trends and opens the door to advanced analytics.

## Project Highlights

### Data Extraction
- Utilized the Alpha Vantage API to fetch daily stock data for IBM.

### Data Preprocessing
- Converted the timestamp column to a datetime format.
- Calculated the moving average for trend analysis.
- Saved the preprocessed data as "processed_stock_data.csv."

### Uploading to Google Drive
- Authentication for accessing and manipulating the Google Drive folder was achieved via a service account key file.
- Essential Python libraries for interacting with Google Drive were installed.

### Apache Airflow DAG
- Created an Apache Airflow Directed Acyclic Graph (DAG) with tasks for data extraction, preprocessing, and upload.
- Scheduled the DAG to run every minute.

### Integration with Power BI
- Connected "processed_stock_data.csv" from Google Drive to Power BI.
- Created various visualizations in Power BI to analyze IBM stock data.

### Potential for Improvement
- This project offers opportunities for further enhancement, such as integrating machine learning models to predict stock trends for investment decisions.

## Getting Started
1. Ensure you have the required Python libraries installed.
2. Set up your service account key file for Google Drive API access.
3. Create an Apache Airflow environment and schedule the DAG for automated data management.
4. Connect your data to Power BI.

## Conclusion
This project showcases the power of Apache Airflow in simplifying complex data workflows. It offers valuable automation and data management capabilities for data engineers and data scientists. The potential for future enhancements, such as predictive analytics, makes it a versatile tool in the realm of data pipelines.

In summary, Apache Airflow is an essential skill for data professionals, significantly improving data workflow management and analysis.
