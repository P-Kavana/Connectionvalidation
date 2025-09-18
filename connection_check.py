import csv
import socket
import sys
import os

if len(sys.argv) < 3:
    print("Usage: python connection_check.py <DRDC_NUMBER> <CSV_FILE>")
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
def check_conn(host, port, timeout=3):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
         return True, ''
    except Exception as e:
        return False,str(e)

def run_conn_check(drdc_number, csv_file):
    result = []
    success_list = []
    failed_list = []
    
    # Fetching the details from csv file
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)

        # Validate the DRDC details exist in fieldnames(cols)
        if drdc_number not in reader.fieldnames:
            print(f"Couldn't find Endpoint details for {drdc_number}")
            return
        
        for row in reader:
            service = row['ServiceName']
            port = row['Port']
            critical = row['Business Critical']
            SF_Component = row['SF_Component']
            host = row.get(drdc_number)

            result = {
                'service': service,
                'critical':critical,
                'SF_Component':SF_component,
                'status': '',
                'error': ''
            }

            if not host:
                result['status'] = 'Connection skipped'
                result['error'] = 'Missing Endpoint value'
                failed_list.append(result)
            
            elif not port:
                result['status'] = 'Connection skipped'
                result['error'] = 'Missing Port number'
                failed_list.append(result)

            else:
                success,error=check_conn(host,port)
                result['status'] = 'Success' if success else 'Failed'
                result['error'] = error

                if success:
                    success_list.append(result)
                else:
                    failed_list.append(result)


    if success_list:
        print("\n✅ Successful Connections:")
        print(f"{'ServiceName':<20} | {'SF_Component':<20} | {'Business Critical':<20} | {'status':<20}")
        for s in success_list:
            print(f"{s['service']:<20} | {s['SF_Component']:<20} | {s['critical']:<20} | {s['status']:<20}")
    if failed_list:
        print("\n❌ Failed Connections:")
        print(f"{'ServiceName':<20} | SF_Component':<20} | {'Business Critical':<20} | {'status':<20} | {'Error'}")
        for f in failed_list:
            print(f"{f['service']:<20} | {s['SF_Component']:<20} | {s['critical']:<20} |{f['status']:<20} | {f['error']}")


if __name__ == "__main__":
    run_conn_check(drdc_number,csv_file)
