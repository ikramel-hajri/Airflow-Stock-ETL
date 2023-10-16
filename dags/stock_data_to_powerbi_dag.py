import requests
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from datetime import datetime
from pytz import UTC
from airflow.utils.dates import days_ago

# Function to fetch stock data from Alpha Vantage
def fetch_stock_data():
    print("Fetching stock data...")
    # Replace 'YOUR_ALPHA_VANTAGE_API_KEY' with your actual Alpha Vantage API key.
    # You can obtain the API key from the Alpha Vantage website.
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    symbol = "IBM"
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&datatype=csv'
    response = requests.get(url)
    with open('stock_data.csv', 'wb') as f:
        f.write(response.content)
        f.close()
    print("Stock data fetched and saved")

# Function to pre-process the stock data
def pre_process_stock_data():
    df = pd.read_csv('stock_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate a 10-period moving average and add it as a new column
    df['Moving Average'] = df['close'].rolling(window=10).mean()
    
    # Export the processed data to a new CSV
    df.to_csv('processed_stock_data.csv', index=False)
    print("Stock data pre-processed and saved")

# Function to upload a file to Google Drive
def upload_file_to_drive(file_path, drive_folder_id, service_account_key_file):
    print(f"Uploading 'processed_stock_data.csv' to Google Drive...")
    credentials = service_account.Credentials.from_service_account_file(service_account_key_file, scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=credentials)
    
    media = MediaFileUpload(file_path, resumable=True)
    
    file_metadata = {
        'name': file_path,
        'parents': [drive_folder_id]
    }
    
    uploaded_file = drive_service.files().create(media_body=media, body=file_metadata).execute()
    
    print(f"File '{uploaded_file['name']}' uploaded to Google Drive with ID: {uploaded_file['id']}")

default_args = {
    'owner':'airflow',
    'start_date': datetime(2023, 10, 15, tzinfo=UTC)
}

dag = DAG(
    dag_id="load_stock_data",
    catchup=False,
    schedule="*/1 * * * *",
    default_args=default_args
)

fetch_stock_data_task = PythonOperator(
    task_id="extract_data",
    python_callable=fetch_stock_data,
    dag=dag
)

pre_process_stock_data_task = PythonOperator(
    task_id="pre_process",
    python_callable=pre_process_stock_data,
    dag=dag
)

upload_file_to_drive_task = PythonOperator(
    task_id="upload_file_to_drive",
    python_callable=upload_file_to_drive,
    op_kwargs={
        "file_path": "processed_stock_data.csv",
        "drive_folder_id": "1pQLteKA_X0FyXklpDis2pg0N3Apdnllw",
        "service_account_key_file": "/root/airflow/dags/token.json"
    },
    dag=dag
)

fetch_stock_data_task >> pre_process_stock_data_task >> upload_file_to_drive_task
