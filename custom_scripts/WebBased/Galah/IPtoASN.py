import pandas as pd
import ipaddress
import os
import glob


INPUT_FOLDER = 'Galah_csv'     
OUTPUT_FOLDER = 'output_results'     
IP_COUNTRY_DB_PATH = 'IP2LOCATION-LITE-DB1.CSV'  

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Reading IP-to-country database...")
try:
    ip_db = pd.read_csv(
        IP_COUNTRY_DB_PATH,
        header=None,
        names=['ip_from', 'ip_to', 'country_code', 'country_name'],
        usecols=[0, 1, 2, 3]
    )
except FileNotFoundError:
    print(f"The file '{IP_COUNTRY_DB_PATH}' was not found.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the IP2Location database: {e}")
    exit(1)

ip_db['ip_from'] = ip_db['ip_from'].astype('uint32')
ip_db['ip_to'] = ip_db['ip_to'].astype('uint32')

ip_db.sort_values('ip_from', inplace=True)
ip_db.reset_index(drop=True, inplace=True)

def ip_to_country(ip):
    try:
        ip_int = int(ipaddress.IPv4Address(ip))
    except ValueError:
        return None  

    left = 0
    right = len(ip_db) - 1
    while left <= right:
        mid = (left + right) // 2
        if ip_db.loc[mid, 'ip_from'] <= ip_int <= ip_db.loc[mid, 'ip_to']:
            return ip_db.loc[mid, 'country_name']
        elif ip_int < ip_db.loc[mid, 'ip_from']:
            right = mid - 1
        else:
            left = mid + 1
    return None

print("Processing CSV files from the input folder...")
csv_files = glob.glob(os.path.join(INPUT_FOLDER, '*.csv'))

if not csv_files:
    print(f"No .csv files found in the folder '{INPUT_FOLDER}'.")
    exit(1)

for file in csv_files:
    try:
        df = pd.read_csv(file)
        print(f"Processing '{file}'...")
    except Exception as e:
        print(f"Error reading '{file}': {e}")
        continue  

    if 'SrcIP' not in df.columns:
        print(f"The column 'SrcIP' was not found in '{file}'. Skipping this file.")
        continue 


    ip_counts = df['SrcIP'].value_counts().reset_index()
    ip_counts.columns = ['SrcIP', 'Count']

    ip_counts['Country'] = ip_counts['SrcIP'].apply(ip_to_country)

    country_counts = ip_counts.groupby('Country')['Count'].sum().reset_index()
    country_counts.sort_values('Count', ascending=False, inplace=True)

    base_filename = os.path.splitext(os.path.basename(file))[0]
    ip_counts_output_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}_ip_counts.csv")
    country_counts_output_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}_country_counts.csv")

    ip_counts.to_csv(ip_counts_output_path, index=False)
    print(f"Most interacting IPs have been written to '{ip_counts_output_path}'.")

    country_counts.to_csv(country_counts_output_path, index=False)
    print(f"Country counts have been written to '{country_counts_output_path}'.\n")
