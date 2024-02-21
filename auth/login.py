import requests;

import info;

url = "https://bus.inje.ac.kr//login_proc.php";

def fn_login():
    username = input("아이디를 입력: ");
    password = input("비밀번호를 입력: ");

    login_form_data = {
        'id': username,
        'password': password,
        's_cookie': 'on'
    };

    with requests.Session() as session:
        post = session.post(url, data=login_form_data);
        info.cookies = session.cookies.get_dict();