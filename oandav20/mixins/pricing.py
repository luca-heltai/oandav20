from account import INSTRUMENTS


class PricingMixin(object):
	"""Methods in PricingMixin class handles the pricing endpoints."""
		
	def get_price_info(self, instruments):
		"""Get price information for 1 or more instruments.
		
		Args:
			instruments (list): Code of instrument(s).
		
		Note:
			Even if instrument code(s) are invalid, Oanda responds with HTTP 
			status 200 and normal JSON Price object, however details won't be 
			provided and thus an instrument code control is needed.
	
		Returns:
			JSON object with price information.
		
		Raises:
			HTTPError: HTTP status code is 4xx or 5xx.
			ValueError: Invalid instrument code passed to the 'instruments' 
				parameter.
		"""
		account_id = self.default_id
		endpoint = "/{}/pricing".format(account_id)
		
		for code in instruments:
			if code in INSTRUMENTS.values():
				continue
			else:
				raise ValueError("Invalid instrument code '{}' passed to the "
					"'instruments' parameter.".format(code))
			
		url_params = {"instruments": ",".join(instruments)}
		response = self.send_request(endpoint, params=url_params)
		
		if response.status_code >= 400:
			response.raise_for_error()
	
		return response.json()
