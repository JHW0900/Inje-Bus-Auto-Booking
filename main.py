import getpass;
from flask import session;

from busAPI import *;
from auth import login;

if __name__ == "__main__":
    username = input("아이디를 입력: ");
    password = getpass.getpass("비밀번호를 입력: ");
