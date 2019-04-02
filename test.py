def main():
    if action == "start":
        startInstance()
    elif action == "stop":
        stopInstance()
    else :
        print"please select the action"
def startInstance():
    response = ec2.start_instances(InstanceIds=[instance_id] )
def stopInstance():
    response = ec2.stop_instances(InstanceIds=[instance_id] )
    
# login call

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "you have been logged out  <a href="/logout"> Logout </a>"
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'aadil123' and request.form['email'] == 'aadil@cosmiclabs.co':
        session['logged_in'] = True
    else:
        flash('wrong password !')
        return home()
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()