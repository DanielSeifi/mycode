import json
import subprocess
import datetime
import socket

date_format = "%Y-%m-%d"  # فرمت تاریخ
today = str(datetime.date.today().strftime(date_format))

def format_date(date_notformat):
    date_obj = datetime.datetime.strptime(date_notformat, "%b %d, %Y")
    date_formated = date_obj.strftime(date_format)
    return str(date_formated)

def calculate_date_difference(date1, date2):
    date1_obj = datetime.datetime.strptime(date1, date_format)
    date2_obj = datetime.datetime.strptime(date2, date_format)
    difference = date2_obj - date1_obj
    return difference.days

def get_users():
    #فیلتر کردن یوزر های 1000 تا 1500 اضافه شود
    users = subprocess.check_output(['awk', '-F:', '$3 >= 1000 && $3 <= 1500 { print $1 }', '/etc/passwd']).decode().split('\n')[:-1]
    print(users)
    return users

def get_password_expiry(username):
    password_info = subprocess.check_output(['chage', '-l', username]).decode().split('\n')
    password_expiry = str(password_info[3].split(": ")[1])
    return password_expiry

def get_last_password_change(username):
    password_info = subprocess.check_output(['chage', '-l', username]).decode().split('\n')
    last_password_change = str(password_info[0].split(": ")[1])
    return last_password_change

def main():
    users = get_users()
    user_data = {}
    for user in users:
        password_expiry = get_password_expiry(user)
        last_password_change = format_date(get_last_password_change(user))
        if password_expiry != 'never':
            password_expiry = format_date(password_expiry)
            difference = calculate_date_difference(today,password_expiry)
        else:
            difference = 9999
        user_data[user] = {'password_expiry': password_expiry, 
                           'last_password_change': last_password_change, 
                           'difference': difference,}
    hostname = socket.gethostname()
    srv_date = {hostname: {'Date': today,
                'Users': user_data,}}
    with open('user_data.json', 'w') as f:
        json.dump(srv_date, f)

if __name__ == '__main__':
    main()