from flask import Flask
import boto
app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

@app.route('/')
def lbs():
	conn = boto.connect_elb(
		aws_access_key_id=app.config['ACCESS_KEY'],
		aws_secret_access_key=app.config['SECRET_KEY']
	)
	load_balancers = conn.get_all_load_balancers(app.config['LOAD_BALANCERS'])
	lbs = []
	for lb in load_balancers:
		instances = lb.get_instance_health()
		lb_status = {
			'name': lb.name,
			'instances': instances,
			'status': 'ok',
		}
		if len(instances) < 2 or not all([i.state == 'InService' for i in instances]):
			lb_status['status'] = 'reduced'
		
		lbs.append(lb_status)
	import pprint
	return pprint.pformat(lbs)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
