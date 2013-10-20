from flask import Flask,g, request
import os, sys
import json
import pdb
from datetime import datetime
from subprocess import call

app = Flask(__name__)
DATABASE = 'deploy.json'

@app.before_request
def before_request():
    try:
        db = open(DATABASE).read()
    except IOError:
        db = '{ "entries" : [] }'
    g.db = json.loads(db)

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        open(DATABASE,'w').write(json.dumps(g.db, indent=4))


def add_entry(form):
    g.db['entries'].insert(0, {
        'committer':form['committer'],
        'before': form['before'],
        'after': form['after'],
	'timestamp':form['timestamp'],
	'pull_time':form['pull_time'],
	'message':form['message'],
        })

@app.route('/eys',methods=['POST'])
def foo():
   try:
	data = json.loads(request.form['payload'])
	if data['ref'] == 'refs/heads/master':
		form_to = {}
   		form_to['committer']=format(data['commits'][0]['author']['name'])
		form_to['before']=format(data['before'])
		form_to['after']=format(data['after'])
		form_to['timestamp']=format(data['commits'][0]['timestamp'])
		form_to['message']=format(data['commits'][0]['message'])
		form_to['pull_time']=format(datetime.now())
		add_entry(form_to)
		call(['deploy_scripts/eys.sh'])
   	return "OK"
   except Exception as e:
	print e
	return "Not Ok"



if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8013,debug=True)
