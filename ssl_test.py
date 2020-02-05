#! /usr/bin/python3

# Author: Roy B
# This program interacts with the Qualys SSL-Labs API to perform SSL tests on endpoints. 
# The program prompts the user for a site analyze, provides on-going status of the scan, and 
# outputs each IP Address and Host for the website with their respective SSL test grade. The user 
# then has to option to request a detailed report from the scan and the detailed report will be written to disk.

import datetime
import json
import requests
import sys
import time

host = input('\nSite to analyze: ')

def initiate_scan():
    url = 'https://api.ssllabs.com/api/v3/analyze?host={}&startNew=on'.format(host) 
    response = requests.get(url)
    response.raise_for_status()  
    data = json.loads(response.text)

    if data['status'] == 'ERROR':
        print('Unable to resolve domain name')
        sys.exit()

    return(data)

def poll_scan():
    i=0
    print('\n' + '-' * 15 + 'STATUS' + '-' * 15 + '\n')
    scan = initiate_scan()
    time.sleep(10.0)
    while scan['status'] != 'READY':
        url = 'https://api.ssllabs.com/api/v3/analyze?host={}'.format(host)
        response = requests.get(url)
        response.raise_for_status()  
        scan = json.loads(response.text)
        print(scan['status'])
        if scan['status'] == 'ERROR':
            print(scan['statusMessage'])
            sys.exit()     
        try:
            print(scan['endpoints'][i]['statusDetailsMessage'])
        except KeyError:
            if scan['status'] != 'READY' and scan['status'] != 'DNS':
                i+=1
                print('Testing Another IP Address')
        time.sleep(10.0)
            
    for i in range(len(scan['endpoints'])):
        try:
            print('\n' + '-' * 50)
            print('Grade: {} \nIp Address: {} \nHost Name: {}'.format(scan['endpoints'][i]['grade'], scan['endpoints'][i]['ipAddress'], scan['endpoints'][i]['serverName']))
            print('-' * 50)
        except KeyError:
            print('Grade: {} \nIp Address: {}'.format(scan['endpoints'][i]['grade'], scan['endpoints'][i]['ipAddress']))
            print('-' * 50)

def get_detailed_scan():
        ip_address = input('IP Address of Host: ')
        url = 'https://api.ssllabs.com/api/v3/getEndpointData?host={}&s={}'.format(host,ip_address) 
        response = requests.get(url)
        response.raise_for_status()  
        scan = json.loads(response.text)
        with open(host + time.strftime("%Y%m%d-%H%M%S") + '.json', 'w', encoding='utf-8') as f:
            json.dump(scan, f, ensure_ascii=False, indent=4)
        print('File saved to disk')    
        #print(json.dumps(scan, indent=4, sort_keys=True))

if __name__ == "__main__":
    poll_scan()
    while True:
        choice = input('\nDo you want a detailed report? Y/N : ')
        if choice.lower() == 'y':
            get_detailed_scan()
            #print('Exiting...\n')
            #sys.exit()
        elif choice.lower() == 'n':
            print('Exiting...\n')
            sys.exit()
        else:
            print('Enter either Y/N')
            continue