from busAPI import *;
from auth import login 
from flask import Flask, render_template, request, session, redirect, url_for, g;
app = Flask(__name__)
app.secret_key = "super secret";
app.config['JSON_AS_ASCII'] = False;

# Main Page
@app.route("/", methods=["GET"])
def main():
    if "cookies" in session:
        print(getBookedBus());
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
    return redirect(url_for("main"));

@app.before_request
def load_logged_in_user():
    if "cookies" in session:
        g.user = True;
    else: g.user = None;

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True);