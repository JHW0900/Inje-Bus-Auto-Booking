from busAPI import *;
from bookAPI import getBookInfo;
from auth import login 
from flask import Flask, render_template, request, session, redirect, url_for, g, flash;
app = Flask(__name__)
app.secret_key = "super secret";
app.config['JSON_AS_ASCII'] = False;
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# Main Page
@app.route("/", methods=["GET"])
def main():
    return render_template("main.html");

# Login Page
@app.route("/login", methods=["GET"])
def login_page():
    if g.user:
        return redirect(url_for("main"));
    return render_template("login.html");

# Login Process
@app.route("/login_proc", methods=["POST"])
def login_proc():
    username = request.form['username'];
    password = request.form['password'];

    res_cookies = login.fn_login(username, password);

    if res_cookies != None:
        session["cookies"] = res_cookies;
        return redirect(url_for("main"));
    else: return redirect(url_for("login_page"));

# Logout Process
@app.route("/logout", methods=["GET"])
def logout():
    session.clear();
    return redirect(url_for("login_page"));

@app.route("/booking", methods=["GET"])
def booking():
    if g.user:
        return render_template("booking.html");
    else:
        return redirect(url_for("login_page"));

@app.route("/book/injeBus", methods=["POST"])
def bookInjeBus():
    if g.user:
        reqData = {
            "line_code": request.form["line_select"],
            "begin_line_sun": "free",
            "end_line_sun": "free",
            "begin_line_sat": "free",
            "end_line_sat": "free",
        };
        days = ("mon", "tue", "wed", "thu", "fri");

        for day in days:
            begin_key = "begin_line_" + day;
            end_key = "end_line_" + day;

            reqData[begin_key] = request.form[begin_key];
            reqData[end_key] = request.form[end_key];

        getBookInfo(reqData);

        msg = "예약이 완료되었습니다.";
        print(msg, "\n");
        flash(msg);
        return redirect(url_for("main"));
    else:
        return redirect(url_for("login_page"));


@app.before_request
def load_logged_in_user():
    if "cookies" in session:
        g.user = True;
    else: g.user = None;

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True);