import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import pandas as pd
import json

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['MONGO_DBNAME'] = 'bank_db'
app.config['MONGO_URI'] = 'mongodb://banker:banker11@ds029911.mlab.com:29911/bank_db'
mongo = PyMongo(app)
col = mongo.db.banks
if col.count() == 0:
	file_res = 'csv_data/bank_branches.csv'
	data = pd.read_csv(file_res)
	records_ = data.to_dict(orient = 'records')
	result = col.insert_many(records_ )

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/ifsc-details', methods=['POST'])
def get_ifsc_details():
	ifsc = request.form['ifsc']
	cur = col.find({"ifsc": ifsc})
	return render_template('bank-details.html', details=cur)

@app.route('/branch-details', methods=['POST'])
def get_branch_details():
	details = request.form
	cur = col.find({"bank_name": details["bank-name"], "city": details["city"]})
	return render_template("bank-details.html", details=cur)

if __name__ == "__main__":
	app.run