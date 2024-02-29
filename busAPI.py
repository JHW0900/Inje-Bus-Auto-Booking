import requests, re;
from bs4 import BeautifulSoup;
from datetime import date, timedelta;
from flask import session

cookies = None;

# 현재 날짜 반환
def getCurDate():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    cur_date = date.today();
    cur_day = days[cur_date.weekday()];

    date_set = {
        "dateCode": cur_date.strftime("%Y%m%d"),
        "curDate": cur_date,
        "curDay": cur_day
    }
    return date_set;

# 다음 날짜 반환
def getNextDate(cur_date):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    next_date = cur_date + timedelta(days=1);
    cur_day = days[next_date.weekday()];

    date_set = {
        "dateCode": next_date.strftime("%Y%m%d"),
        "curDate": next_date,
        "curDay": cur_day
    }
    return date_set;

# 요청된 날짜에 해당하는 예약 가능 지역 조회
def getLine(date_code):
    url = "https://bus.inje.ac.kr/reserve/day_select_proc.php"
    data = { "dateCode": date_code };
    cookies = session["cookies"];

    res = requests.post(url, data, cookies=cookies);

    if res.status_code == 200:
        line_dict = {};
        line_str = res.json()["lineList"].replace("양산 - 물금", "양산-물금").replace("양산 - 북정", "양산-북정");
        line_str = line_str.replace("영도/부산역", "부산역");
        parse_str = re.sub(r"[^0-9가-힣\-]", " ", line_str).replace("노선선택", "").strip(" ");
        parse_list = re.sub(" +", " ", parse_str).split(" ");

        line_dict["status"] = res.json()["status"];
        for i in range(0, len(parse_list) - 1, 2):
            key = parse_list[i];
            val = parse_list[i + 1];
            line_dict[key] = val;

        return line_dict;

# 해당 날짜에 예약 가능한 시간을 조회
def getTime(line_code, date_code):
    url = "https://bus.inje.ac.kr/reserve/time_select_proc.php";
    data = {
        "lineCode": line_code, 
        "dateCode": date_code
    };
    cookies = session["cookies"];

    res = requests.post(url, data, cookies=cookies);

    if res.status_code == 200:
        time_list = [];
        time_str = res.json()["list"].replace("양산 - 물금", "양산-물금").replace("양산 - 북정", "양산-북정");
        time_str = time_str.replace("영도/부산역", "부산역");
        parse_str = re.sub(r"[^0-9가-힣\-]", " ", time_str).replace("노선선택", "").strip(" ");
        parse_list = re.sub(" +", " ", parse_str).split(" ");

        for i in range(0, len(parse_list) - 5, 6):
            time_dict = {};
            time_dict["busCode"] = parse_list[i + 1];
            time_dict["busType"] = parse_list[i + 2];
            time_dict["busTime"] = parse_list[i + 3] + ":" + parse_list[i + 4];
        
            time_list.append(time_dict);
        
        return time_list;

# 버스 busCode 조회
def getBusCode(line_code, time_code):
    url = "https://bus.inje.ac.kr/reserve/select_seat.php";
    params = {
        "lineCode": line_code,
        "timeCode": time_code
    };
    cookies = session["cookies"];

    res = requests.get(url, cookies=cookies, params=params);
    soup = BeautifulSoup(res.text, "html.parser");
    seats = soup.select(".ui-grid-d > div > a");
    for seat in seats:
        if seat.get_text() == "X":
            continue;
        
        func = str(seat["onclick"]);
        bus_code = re.sub(" +", " ", re.sub(r"[^0-9]", " ", func).strip(" ")).split(" ")[0];
        break;
    
    return bus_code;

# 버스 예약
def bookBus(bus_code, seatNum):
    url = "https://bus.inje.ac.kr/reserve/insert_reserve_proc.php";
    data = {
        "busCode": bus_code,
        "seatNum": seatNum,
        "oriCode": bus_code
    };
    cookies = session["cookies"];

    is_done = False;
    while not is_done:
        res = requests.post(url, data, cookies=cookies);
        seat_num = int(data["seatNum"]);
        status = res.json()["status"];
        msg = res.json()["message"];

        print("[", status, "]", seat_num, "번 좌석", msg);
        
        if msg == "예약은 차량출발 1시간 전까지 가능합니다.": break;

        if status == "success":
            print(str(seat_num), "번 좌석 예약 완료");
            is_done = True;
        
        elif msg == "이미 선택된 좌석입니다.":
            seat_num += 1;
            if seat_num > 44: seat_num = 1;
            data["seatNum"] = seat_num;
        else: break;
    return is_done;

# 예약된 버스 조회
def getBookedBus():
    url = "https://bus.inje.ac.kr/index.php";
    cookies = session["cookies"];
    
    res = requests.get(url, cookies=cookies);
    soup = BeautifulSoup(res.text, "html.parser");

    root_selector = "#extends > div > ul > li";
    info_selector = root_selector + " > a";

    info_list = soup.select(info_selector);

    bus_list = [];
    for i in range(0, len(info_list), 2):
        bus_info = {};

        el_info = info_list[i];
        el_code = info_list[i + 1];

        p_info_list = el_info.find_all("p");
        bus_info["info_date"] = el_info.h2.get_text().replace("\xa0", " ");
        bus_info["info_line"] = p_info_list[0].get_text();
        bus_info["info_bus"] = p_info_list[1].get_text();
        bus_info["info_cancel"] = p_info_list[2].get_text();

        cancel_info = re.sub(" +", " ", re.sub(r"[^0-9NY]", " ", el_code["onclick"]).strip(" ")).split(" ");
        bus_info["cancel_code"] = cancel_info[0];
        bus_info["cancel_type"] = cancel_info[1];

        bus_list.append(bus_info);
    return bus_list;

# 예약된 버스 일괄 취소
def cancelAllBooking():
    bus_list = getBookedBus();
    url = "https://bus.inje.ac.kr/reserve/cancel_proc.php";
    cookies = session["cookies"];
    
    for el in bus_list:
        data = {
            "seq": el["cancel_code"]
        };

        if el["cancel_type"] == "N":
            res = requests.post(url, data, cookies=cookies);
            print(res.text);
        else:
            print(res.text, "해당내역은 증차된 차량이며, 예약취소시 패널티가 부여됩니다.\n취소를 원하시면, 본 사이트에서 계속해주세요.")
