import getpass;
import requests;

import busAPI;

url = "https://bus.inje.ac.kr/login_proc.php";

def fn_login():
    while True:
        username = input("아이디를 입력: ");
        password = getpass.getpass("비밀번호를 입력: ");

        login_form_data = {
            'id': username,
            'password': password,
            's_cookie': 'on'
        };

        with requests.Session() as session:
            res = session.post(url, data=login_form_data);
            res_set = res.json();
            busAPI.session = session;

            if res_set["status"] == "success": 
                print(res_set["message"]);
                break;
            else:
                print("로그인 실패:", res_set["message"], "\n");