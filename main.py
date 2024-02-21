import requests
import time
import json

import info
from auth import login;

if __name__ == "__main__":
    login.fn_login();

    url = info.url
    cookies = info.cookies;
    data = info.data;

    is_done = False;

    while not is_done:
        res = requests.post(url=url, cookies=cookies, data=data)
        seat_num = int(data["seatNum"]);
        status = res.json()["status"];
        msg = res.json()["message"];

        print("[", status, "]", seat_num, "번 좌석", msg);
        
        if msg == "예약은 차량출발 1시간 전까지 가능합니다.": break;

        if status == "success":
            print(str(seat_num), "번 좌석 예약 완료");
            is_done = True;
        else:
            seat_num += 1;
            if seat_num > 44: seat_num = 1;
            data["seatNum"] = seat_num;