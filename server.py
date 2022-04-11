from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
import pprint

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)
