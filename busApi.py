import requests, re;
from datetime import date, timedelta;

session = None;

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

def getLine(date_code):
    url = "https://bus.inje.ac.kr/reserve/day_select_proc.php"
    data = { "dateCode": date_code };

    res = session.post(url, data);

    if res.status_code == 200:
        line_dict = {};
        line_str = res.json()["lineList"];
        parse_str = re.sub(r"[^0-9가-힣]", " ", line_str).replace("노선선택", "").strip(" ");
        parse_list = re.sub(" +", " ", parse_str).split(" ");

        for i in range(0, len(parse_list) - 1, 2):
            key = parse_list[i];
            val = parse_list[i + 1];
            line_dict[key] = val;
        
        return line_dict;

# 해당 날짜의 예약 가능한 시간을 조회
def getTime(line_code, date_code):
    url = "https://bus.inje.ac.kr/reserve/time_select_proc.php";
    data = {
        "lineCode": line_code, 
        "dateCode": date_code
    };

    res = session.post(url, data);
    print(res.json());

# 버스 예약
def bookBus():
    url = "https://bus.inje.ac.kr/reserve/insert_reserve_proc.php";
    data = {
        "busCode": "110665",
        "seatNum": "1",
        "oriCode": "110665"
    }

    is_done = False;
    while not is_done:
        res = session.post(url, data)
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