import requests;
import logging
import info;

def getTime():
    session = info.session;
    url = "https://bus.inje.ac.kr/reserve/time_select_proc.php";
    cookies = info.cookies;
    headers = {
        'Content-Type': 'application/json',
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "lineCode": "8", 
        "dataCode": "20240224"
    };

    res = session.get(url=url, headers=headers, data=data);
    print(res.text);