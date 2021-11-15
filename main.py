import os
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    wd = os.getcwd()
    os.chdir("/")
    p = subprocess.Popen('python3 run test', cwd= wd + '/ScoreCalculator', shell=True)
    p.wait()

    path = wd + '/ScoreCalculator/output.txt'
    with open(path, 'r') as f:
        data = f.read()


    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))