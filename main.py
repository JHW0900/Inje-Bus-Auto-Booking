import requests
import time

import info

url = info.url
cookies = info.cookies;
data = info.data;

is_done = False;

while not is_done:
    res = requests.post(url=url, cookies=cookies, data=data)
    seat_num = int(data["seatNum"]);

    if str(res) == "<Response [200]>":
        print(str(seat_num), "번 좌석 예약 완료");
        is_done = True;
    else:
        seat_num += 1;
        if seat_num > 44: seat_num = 1;
        data["seatNum"] = seat_num;