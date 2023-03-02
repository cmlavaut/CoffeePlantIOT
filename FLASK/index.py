from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host= "192.168.50.155",port = 5000 , debug = True)
