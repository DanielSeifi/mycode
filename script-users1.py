import json
import subprocess
import datetime

def get_users():
    #فیلتر کردن یوزر های 1000 تا 1500 اضافه شود
    users = subprocess.check_output(['awk', '-F:', '$3 >= 1000 && $3 <= 1500 { print $1 }', '/etc/passwd']).decode().split('\n')[:-1]
    print(users)
    return users

def get_password_expiry(username):
    password_info = subprocess.check_output(['chage', '-l', username]).decode().split('\n')
    password_expiry = password_info[3].split(': ')[1]
    return password_expiry

def get_last_password_change(username):
    password_info = subprocess.check_output(['chage', '-l', username]).decode().split('\n')
    last_password_change = password_info[0].split(': ')[1]
    return last_password_change

def main():
    users = get_users()
    user_data = {}
    for user in users:
        password_expiry = get_password_expiry(user)
        last_password_change = get_last_password_change(user)
        user_data[user] = {'password_expiry': password_expiry, 'last_password_change': last_password_change}
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

if __name__ == '__main__':
    main()