from system.core.model import *
import re # still need to import this module: we use regular expressions to validate email formats!
class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def create_user(self, info):
		# we write our validations in model functions.
		# They will look similar to those we wrote in Flask
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		errors = []
		# some basic validation
		if not info['name']:
			errors.append('Name cannot be blank!')
		elif len(info['name']) < 2:
			errors.append('Name must be at least 2 characters long!')
		if not info['email']:
			errors.append('Email cannot be blank!')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid!')
		if not info['password']:
			errors.append('Password cannot be blank!')
		elif len(info['password']) < 8:
			errors.append('Password must be at least 8 characters long!')
		elif info['password'] != info['pw_conf']:
			errors.append('Password and confirmation must match!')
		# if we hit errors, return them, else return True
		if errors:
			return {"status": False, "errors": errors}
		else:
			password = info['password']
			# bcrypt is now an attribute of our model
			# we will call the bcrypt functions similarly to how we did before
			# here we use generate_password_hash() to generate an encrypted password
			hashed_pw = self.bcrypt.generate_password_hash(password)
			create_query = "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
			create_data = [info['name'], info['email'], hashed_pw]
			self.db.query_db(create_query, create_data)
			# then retrieve the last inserted user
			get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
			users = self.db.query_db(get_user_query)
			return {"status": True, "user": users[0]}

	def login_user(self, info):
		password = info['password']
		user_query = "SELECT * FROM users WHERE email = %s LIMIT 1"
		user_data = [info['email']]
		users = self.db.query_db(user_query, user_data)
		if users[0]:
			# check_password_hash() compares encrypted password in DB to one provided by users logging in
			if self.bcrypt.check_password_hash(users[0]['password'], password):
				return users[0]
		# Whether we did not find the email, or if the password did not match, either way return False
		return False