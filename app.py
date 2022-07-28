from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

if __name__ == "__main__":
    app.run()