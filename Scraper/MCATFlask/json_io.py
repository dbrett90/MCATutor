#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/output')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	result = ''

	for item in data:
		# loop over every row
		userResponse = str(item['input'])
		print("user response:")
		print(userResponse)
		if(userResponse == 'Platypus'):
			result += 'Hi Platypus'
		else:
			result += 'Hi'

	return json.dumps({'botResponse' : result})

if __name__ == '__main__':
	app.debug = True
	# run!
	app.run()