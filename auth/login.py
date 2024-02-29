import getpass;
import requests;
import busAPI;
from flask import flash;

url = "https://bus.inje.ac.kr/login_proc.php";

def fn_login(username, password):
    ret_cookies = None;
    while True:
        # username = input("아이디를 입력: ");
        # password = getpass.getpass("비밀번호를 입력: ");

        login_form_data = {
            'id': username,
            'password': password,
            's_cookie': 'on'
        };

        with requests.Session() as session:
            res = session.post(url, data=login_form_data);
            res_set = res.json();
            busAPI.cookies = session.cookies.get_dict();

            if res_set["status"] == "success": 
                print(res_set["message"]);
                ret_cookies = busAPI.cookies;
            else:
                fail_msg = "로그인 실패: " + res_set["message"];
                print(fail_msg, "\n");
                flash(fail_msg);
            break;
    return ret_cookies;