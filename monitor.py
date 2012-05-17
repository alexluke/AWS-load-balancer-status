from flask import Flask
from flask import render_template
import boto
app = Flask(__name__)
app.config.from_pyfile('settings.cfg')

@app.template_filter()
def yesno(value, yes, no):
	if value:
		return yes
	return no

@app.route('/')
def elb_status():
	conn = boto.connect_elb(
		aws_access_key_id=app.config['ACCESS_KEY'],
		aws_secret_access_key=app.config['SECRET_KEY']
	)
	load_balancers = conn.get_all_load_balancers(app.config['LOAD_BALANCERS'])
	lbs = []
	for lb in load_balancers:
		instances = []
		for inst in lb.get_instance_health():
			instances.append({
				'id': inst.instance_id,
				'up': inst.state == 'InService',
			})
		lb_status = {
			'name': lb.name,
			'instances': instances,
			'redundant': True,
		}
		if len(instances) < 2 or not all([i['up'] for i in instances]):
			lb_status['redundant'] = False
		
		lbs.append(lb_status)
	return render_template('elb_status.html', lbs=lbs)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
