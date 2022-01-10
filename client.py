import argparse
import requests

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('token', type=str,
					help='token for auth')
parser.add_argument('server', type=str,
					help='server address')
parser.add_argument('job', type=str,
					help='job')
parser.add_argument('action', type=str,
					help='action to execute')

args = parser.parse_args()

r  = requests.post(args.server, data={'token': args.token})
data = r.json()

if data['ok']:
	print('ok')
else:
	print(data['error'])
