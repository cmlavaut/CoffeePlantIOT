from flask import Flask, render_template, redirect, url_for
from threading import Thread
import time


app = Flask(__name__)
x = 5
xx = 1
y = "annie"
z = "manila"

def actualizar():
    global xx
    while True:
        xx +=1
        time.sleep(1)

@app.route('/suma')
def suma():
    global x
    x += 5
    return redirect(url_for("main"))

@app.route('/')
def index():
    hilo = Thread(target=actualizar)
    hilo.start()
    return redirect(url_for("main"))




@app.route('/main')
def main():
    global x, xx
    content = {
        "x" : x,
        "y" : y,
        "z" : z,
        "xx" : xx
    }
    return render_template("index.html", **content)

if __name__ == "__main__":
    app.run(debug = True)
