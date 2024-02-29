from busAPI import *;
from datetime import datetime;

# 지역 (창원)
line_code = "8";

# 원하는 좌석
seat_num = 1;

# 제일 빠른 수업 시간
tmp_begin_data = {
    "Sun": "free",
    "Mon": "08:00",
    "Tue": "08:00",
    "Wed": "free",
    "Thu": "08:00",
    "Fri": "08:00",
    "Sat": "free",
}

# 마지막 수업 종료 시간
tmp_end_data = {
    "Sun": "free",
    "Mon": "17:20",
    "Tue": "free",
    "Wed": "free",
    "Thu": "18:20",
    "Fri": "16:20",
    "Sat": "free",
}

def getBookInfo():
    date_set = getCurDate();

    while True:
        cur_date = date_set["curDate"];
        cur_day = date_set["curDay"];
        date_code = date_set["dateCode"];

        line_set = getLine(date_code);
        if line_set["status"] == "error":
            break;
        elif tmp_begin_data[cur_day] == "free" or not line_set.get(line_code):
            date_set = getNextDate(cur_date);
            continue;
        
        time_list = getTime(line_code, date_code);
        
        # e: {'busCode': '39887', 'busType': '등교', 'busTime': '08:00'}
        begin_time = tmp_begin_data[cur_day];
        end_time = tmp_end_data[cur_day];

        print("=======================");
        print("****", date_code, "****");
        for e in time_list:
            bus_type = e["busType"];
            bus_time = e["busTime"];

            if bus_type == "등교" and bus_time == begin_time:
                print("등교: ");
                bus_code = getBusCode(line_code, e["busCode"]);
                print("탑승 시간:", bus_time);
                bookBus(bus_code, seat_num);
            elif bus_type == "하교" and bus_time == end_time:
                print("하교: ");
                bus_code = getBusCode(line_code, e["busCode"]);
                print("탑승 시간:", bus_time);
                bookBus(bus_code, seat_num);
        print("=======================");
                
        date_set = getNextDate(cur_date);