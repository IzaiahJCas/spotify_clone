import argparse
import sys 
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/members")
def member():
    return {"members": ["1", "2", "3"]}

if __name__ == "__main__":
    app.run(debug=True)