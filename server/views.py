import os
from server import app
from json import dumps
from flask import request
import server.config as config


@app.route('/')
def index():
	return "Hello, HTTPrun loaded and active!"


@app.route('/<job_name>/<action_name>')
def run_job(job_name, action_name):
	token = request.args.get('token', request.form.get('token'))
	if not token:
		return dumps({'ok': False, 'error': 'Access denied'})
	
	jobs = config.CONFIG.get('jobs', {})
	job = jobs.get(job_name, {})
	tokens = job.get('tokens', [])
	if token not in tokens:
		return dumps({'ok': False, 'error': 'Access denied'})

	# Now were safe
	actions = job.get('actions', {})
	action = actions.get(action_name, {})
	if not action:
		return dumps({'ok': False, 'error': 'Action not found'})
	
	print('starting job:"%s" action:"%s"' % (job_name, action_name))
	
	commands = action.get('commands', '').strip().split('\n')
	
	# Making iptables commands
	firewall_rules_set = action.get('firewall')
	for rule in firewall_rules_set:
		command = 'iptables' if rule.get('type', 'v4') == 'v4' else 'ip6tables'
		port = str(int(rule['port']))
		fw_action = rule.get('action', 'open')
		proto = rule.get('proto', 'tcp')
		command += ' -A' if fw_action == 'open' else ' -D'
		command += f' INPUT -p {proto} --dport {port} -j ACCEPT'
		command += f' -s {rule["source"]}' if rule.get('source') else ''
		command += f' -d {rule["dest"]}' if rule.get('dest') else ''
		commands.append(command)
	

	# Executing shell commands
	for command in commands:
		print('running command:"%s"' % command)
		os.system(command)
	
	print('executed job:"%s" action:"%s"' % (job_name, action_name))
	return {'ok': True}
