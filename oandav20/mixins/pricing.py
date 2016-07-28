class PricingMixin(object):
	"""Methods in PricingMixin class handles the pricing endpoints."""

	def get_price_info(self, instruments):
		"""Get price information for 1 or more instruments.
		
		Args:
			instruments (list): Code of instrument(s).
		
		Note:
			Even if instrument code(s) are invalid, Oanda responds with an
			HTTP status 200 and an normal JSON Price object, however details
			won't be provided and thus an instrument code control is needed.
			
		Returns:
			JSON object with price information.
		
		Raises:
			CodeError: pass
			OandaError: pass
		"""
		account_id = self.default_id
		endpoint = "/{}/pricing".format(account_id)
		
		for code in instruments:
			pass
			
		instruments = ",".join(instruments)
		url_params = {"instruments": instruments}
		response = self.send_request(endpoint, params=url_params)
		
		if response.status_code >= 400:
			# raise OandaError with appropriate message
			pass
	
		return response.json()
