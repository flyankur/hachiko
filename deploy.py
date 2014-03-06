'''
Hachiko - A very simple continous integration app built on Flask
Fork Hachiko at https://github.com/flyankur/hachiko
'''

from raven.contrib.flask import Sentry
from flask import Flask,g, request
import os, sys
import json
import pdb
from datetime import datetime
from subprocess import call

app = Flask(__name__)
DATABASE = 'deploy.json'

app.config['SENTRY_DSN'] = 'http://9e5c9bcbe19a489ba3d2a908ca6a1faf:a47b3d8798834f1aa9eea83f9e16cdbd@67.207.152.121:80/8'
sentry = Sentry(app)

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

@app.route('/pull',methods=['POST'])
def foo():
    try:
        data = json.loads(request.form['payload'])
        if data['ref'] == 'refs/heads/development':
		form_to = {}
   		form_to['committer']=format(data['commits'][0]['author']['name'])
		form_to['before']=format(data['before'])
		form_to['after']=format(data['after'])
		form_to['timestamp']=format(data['commits'][0]['timestamp'])
		form_to['message']=format(data['commits'][0]['message'])
		form_to['pull_time']=format(datetime.now())
            	add_entry(form_to)
            	try:
			if data['repository']['url'] == 'https://github.com/pixpa/studio':
				file_to_execute = '/home/experiments/hachiku/studio.sh'
			elif data['repository']['url'] == 'https://github.com/pixpa/sarjak':
				file_to_execute = '/home/experiments/hachiku/sarjak.sh'
			elif data['repository']['url'] == 'https://github.com/pixpa/pixpa.com':
				file_to_execute = '/home/experiments/hachiku/pixpa.com.sh'
                	with open(file_to_exectue):
                		call([file_to_execute])
            	except IOError:
                	raise Exception('Oh dear. You need to copy dummy deploye script in deploy_script folder ( eys.sh ) as deploy.sh in root folder')
        return "OK"
    except Exception as e:
	print e
	sentry.captureMessage("Hachiku ! WTF !")
	sentry.captureException()
	return "Not Ok"



if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8013,debug=True)
