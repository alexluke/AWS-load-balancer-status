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
				'name': get_instance_name(inst.instance_id),
			})
		lb_status = {
			'name': lb.name,
			'instances': instances,
			'redundant': True,
			'serving': True,
		}
		if len(instances) < 2 or not all([i['up'] for i in instances]):
			lb_status['redundant'] = False
		if len([i['up'] for i in instances]) == 0:
			lb_status['serving'] = False
		
		lbs.append(lb_status)
	return render_template('elb_status.html', lbs=lbs)

def get_instance_name(instance_id):
	conn = boto.connect_ec2(
		aws_access_key_id=app.config['ACCESS_KEY'],
		aws_secret_access_key=app.config['SECRET_KEY']
	)
	reservations = conn.get_all_instances([instance_id])
	instances = [i for r in reservations for i in r.instances]
	if len(instances) != 1:
		return None
	return instances[0].tags.get('Name', '')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
