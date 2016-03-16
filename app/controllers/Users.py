from system.core.controller import *
class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		# Note that we have to load the model before using it in the methods below
		self.load_model('User')
	# Method to display registration page
	def index(self):
		return self.load_view('index.html')
	def create(self):
		# gather data posted to our create method and format it to pass it to the model
		user_info = {
			"name": request.form['name'],
			"email": request.form['email'],
			"password": request.form['password'],
			"pw_conf": request.form['pw_conf']
		}
		# call create_user method from model and write some logic based on the returned value
		# notice how we passed the user_info to our model method
		create_status = self.models['User'].create_user(user_info)
		if create_status['status'] == True:
			# The user should have been created in the model
			# we can set the newly-created users id and name to session
			session['id'] = create_status['user']['id']
			session['name'] = create_status['user']['name']
			# we can redirect to the users profile page here
			return redirect('/users/result')
		else:
			# set flashed errors messages here
			for message in create_status['errors']:
				flash(message, 'regis_errors')
			# redirect to the method that renders the form
			return redirect('/')
	def result(self):
		#show the new user that was just created
		flash('User successfully created!')
		return self.load_view('new.html')

	def login(self):
		# log in an existing user
		user_info = {
			"email": request.form['email'],
			"password": request.form['password']
		}
		user = self.models['User'].login_user(user_info)
		if user == False:
			flash('You put in incorrect information!')
			return redirect('/')
		flash('You have successfully logged in!')
		return self.load_view('new.html', user=user)

	# This method logs out a user
	def logout(self):
		session.clear()
		return redirect('/')