import requests

from mixins.account import AccountMixin
from mixins.pricing import PricingMixin


class Oanda(AccountMixin, PricingMixin):
	"""Oanda is the only (main) class, which should be used by user.
	
	It consist of several inherited mixins which extends funcionality of this 
	class. Each mixin covers thematic endpoints, eg. one for orders handling, 
	another for getting account information etc.
	
	Oanda allows to users to have 1 or more trading (sub)accounts. For those 
	who manage only 1 may be too explicit to pass every time the account ID 
	to methods for constructing a URL path. Moreover, there are endpoints 
	where passing any account ID would lead to the same results.
		
	Therefore a 'default_id' attribute will be used for these situations unless 
	the use user provide an different ID to the methods.
		
	Attrs:
		__base_url (str): Prefix for all endpoints.
		__client (object): Session object with HTTP persistent connection to 
			the Oanda API server.
		default_id (str): Oanda account ID.
	"""
	
	def __init__(self, environment, access_token, default_id):
		"""Initialize an instance of class Oanda. 
		
		Args:
			environment (str): Accepts only "demo" or "real".
			access_token (str): Access token for user authentication.
			default_id (str): Oanda account ID.
		
		Raises:
			ValueError: "demo" or "real" wasn't passed to 'environment' 
				parameter.
		"""
		if environment == "demo":
			self.__base_url = "https://api-fxpractice.oanda.com/v3/accounts"
		elif environment == "real":
			self.__base_url = "https://api-fxtrade.oanda.com/v3/accounts"
		else:
			raise ValueError("Invalid argument passed to the 'environment' "
				"parameter.")

		self.__client = requests.Session()
		self.__client.headers["Authorization"] = "Bearer " + access_token
		self.__client.headers["Content-Type"] = "application/json"
		
		self.default_id = default_id
		
	def send_request(self, endpoint, method="GET", **kwargs):
		"""Send an HTTP request to the Oanda server.
		
		User may also use this method for accessing another endpoints which 
		aren't covered in this package.
		
		Args:
			endpoint (str): Suffix of a URL.
			method (str, optional): HTTP method written in capital letters.
			**kwargs: Same keywords arguments like for 'request' object from 
				'requests' package.
		
		Returns:
			HTTP Response object from 'requests' package.
		"""
		url = self.__base_url + endpoint
		
		return self.__client.request(method, url, **kwargs)
