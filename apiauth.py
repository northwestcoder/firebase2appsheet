from functools import wraps
from flask import request, abort
import client

# decorator function
def require_apikey(view_function):
	@wraps(view_function)
	# the new, post-decoration function. Note *args and **kwargs here.
	def decorated_function(*args, **kwargs):
		if request.headers.get('x-apikey') and request.headers.get('x-apikey') == client.instance_apikey:
			return view_function(*args, **kwargs)
		else:
			abort(401)
	return decorated_function