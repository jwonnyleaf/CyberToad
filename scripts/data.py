import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

SCRIPT_NAME = "CyberToad - data.py"
CSV_CIC_DATASET_URL = "http://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/Dataset/CSV/MERGED_CSV/"
PCAP_CIC_DATASET_URL = "http://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/Dataset/PCAP/"
RAW_CIC_CSV_PATH = "./data/raw/CIC_IOT_CSV_Dataset"
PROCESSED_CIC_CSV_FILE_PATH = "./data/processed/CIC_IOT_CSV_Dataset.csv"
RAW_CIC_PCAP_PATH = "./data/raw/CIC_IOT_PCAP_Dataset"
PROCESSED_CIC_PCAP_PATH = "./data/processed/CIC_IOT_PCAP_Dataset"

# Create the directory if it doesn't exist
os.makedirs(RAW_CIC_CSV_PATH, exist_ok=True)
os.makedirs(os.path.dirname(PROCESSED_CIC_CSV_FILE_PATH), exist_ok=True)

def get_files(url, ext="", type="file"):
    """Fetches a list of CSV files from the dataset URL."""
    if type == "file":
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [link.get('href') for link in soup.find_all('a') if link.get('href').endswith(ext)]
    if type == "dir":
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('/') and not link.get('href').startswith('?')]

def download_file(url, save_path):
    """Downloads a file from a URL with a progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(save_path, 'wb') as file, tqdm(
        desc=save_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        leave=True,
        dynamic_ncols=True
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

def process_csv_files():
    """Combines the downloaded CSV files into a single DataFrame."""
    SKIP_DOWNLOAD = False
    csv_files = get_files(CSV_CIC_DATASET_URL, ".csv")
    df_list = []

    # If files already exist in the directory, ask if they should be deleted
    if os.listdir(RAW_CIC_CSV_PATH):
        print(f"[{SCRIPT_NAME}] Files already exist in {RAW_CIC_CSV_PATH}.")
        response = input("\t* Would you like to delete and re-download them? (y/n): ")
        if response.lower() == 'y':
            for file in os.listdir(RAW_CIC_CSV_PATH):
                os.remove(os.path.join(RAW_CIC_CSV_PATH, file))
        else:
            print(f"[{SCRIPT_NAME}] Skipping download.")
            SKIP_DOWNLOAD = True

    if not SKIP_DOWNLOAD:
        for file in csv_files:
                file_url = f"{CSV_CIC_DATASET_URL}{file}"
                save_path = os.path.join(RAW_CIC_CSV_PATH, file)
                download_file(file_url, save_path)
    
    print(f"[{SCRIPT_NAME}] Processing CSV files...")
    with tqdm(total=len(csv_files), desc="Processing CSV files", unit="file", dynamic_ncols=True) as pbar:
        for file in os.listdir(RAW_CIC_CSV_PATH):
            file_path = os.path.join(RAW_CIC_CSV_PATH, file)
            df = pd.read_csv(file_path)
            df.dropna(inplace=True)
            df_list.append(df)
            pbar.update(1)

    # If there is a merged dataset already, ask if it should be deleted
    if os.path.exists(PROCESSED_CIC_CSV_FILE_PATH):
        print(f"[{SCRIPT_NAME}] Merged dataset already exists at {PROCESSED_CIC_CSV_FILE_PATH}.")
        response = input("\t* Would you like to delete and re-merge the datasets? (y/n): ")
        if response.lower() == 'y':
            os.remove(PROCESSED_CIC_CSV_FILE_PATH)
        else:
            print(f"[{SCRIPT_NAME}] Skipping merge.")
            return
        
    start_time = time.time()
    print(f"[{SCRIPT_NAME}] Combining {len(df_list)} datasets, this may take a while...")
    with tqdm(total=len(df_list), desc="Merging CSV files", unit="file", dynamic_ncols=True) as pbar:
        combined_df = pd.concat(df_list, ignore_index=True)
        pbar.update(len(df_list))

    combined_df.to_csv(PROCESSED_CIC_CSV_FILE_PATH, index=False)
    print(f"[{SCRIPT_NAME}] Combined Dataset saved to {PROCESSED_CIC_CSV_FILE_PATH} in {time.time() - start_time:.2f} seconds.")
    print(f"\t* Dataset contains {combined_df.shape[0]} rows and {combined_df.shape[1]} columns.")

def process_pcap_files():
    """Downloads all PCAP files."""
    print(f"[{SCRIPT_NAME}] Fetching list of PCAP directories...")
    pcap_dirs = get_files(PCAP_CIC_DATASET_URL, type="dir")
    print(f"[{SCRIPT_NAME}] Found {len(pcap_dirs)} directories.")

    for directory in pcap_dirs:
        dir_url = f"{PCAP_CIC_DATASET_URL}{directory}"
        save_dir = os.path.join(RAW_CIC_PCAP_PATH, directory)
        os.makedirs(save_dir, exist_ok=True)

        pcap_files = get_files(dir_url, ".pcap")
        with tqdm(total=len(pcap_files), desc=f"Downloading PCAP files from {directory}", unit="file", dynamic_ncols=True) as pbar:
            for file in pcap_files:
                file_url = f"{dir_url}{file}"
                save_path = os.path.join(save_dir, file)
                download_file(file_url, save_path)
                pbar.update(1)

    print(f"[{SCRIPT_NAME}] PCAP files downloaded successfully.")

def print_menu():
    print("""
        ========================================
        CyberToad IoT Dataset Processing Tool
        ========================================
        Select an option:
        [1] Process CSV Files (Download & Merge)
        [2] Download PCAP Files
        [0] Exit
        ========================================
        """)
    
def main():
    print_menu()
    while True:
        choice = input(f"[{SCRIPT_NAME}] Enter Your Choice: ")
        if choice == '1':
            process_csv_files()
            print_menu()
        elif choice == '2':
            process_pcap_files()
            print_menu()
        elif choice == '0':
            print(f"[{SCRIPT_NAME}] Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()
