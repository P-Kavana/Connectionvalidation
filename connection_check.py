import csv
import socket
import sys
import os

if len(sys.argv) < 2:
    print("Missing DRDC Number")
    sys.exit(1)

if len(sys.argv) < 3:
    print("error: Missing endpoint details to parse")
    sys.exit(1)

drdc_number = sys.argv[1].upper()
csv_file = sys.argv[2]

if not (drdc_number.startswith("DC") and drdc_number[2:].isdigit()):
    print(f"Invalid DRDC number format: {drdc_number}")
    sys.exit(1)

if not os.path.exists(csv_file):
    print(f"Couldn't find input file {csv_file}")
    exit(1)

#Checking a TCP connection
def check_conn(host, port, timeout=5):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
         return True, ''
    except Exception as e:
        return False,str(e)

def run_conn_check(drdc_number, csv_file):
    results = []
    
    # Fetching the details from csv file
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)

        # Validate the DRDC details exist in fieldnames(cols)
        if drdc_number not in reader.fieldnames:
            print(f"Couldn't find Endpoint details for {drdc_number}")
            return
        
        for row in reader:
            service = row['service'].strip()
            host = row.get(drdc_number, '').strip()
            port = row.get(drdc_number)

            if not host:
                status = ''
                error='Missing Endpoint value'
            else:
                success,error=check_conn(host)
                status='Connection Successful' if success else 'Connection Failed'

            results.append({
                'service': service,
                'status': status,
                'error': error
            })

    print(f"\nConnectivity results for: {drdc_number} \n")
    for r in results:
        print(f"{r['service']} --> {r['status']} {r['error']}")

if __name__ == "__main__":
    run_conn_check(drdc_number,csv_file)