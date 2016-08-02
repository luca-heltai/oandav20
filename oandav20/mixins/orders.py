from account import INSTRUMENTS

ORDER_TYPE = ["MARKET", "LIMIT", "STOP", "MARKET_IF_TOUCHED"]
SIDE = ["BUY", "SELL"]
TIME_IN_FORCE = ["FOK", "IOC", "GTC", "GTD", "GFD"]


class OrdersMixin:
	"""Methods in the OrdersMixin class handles the orders endpoints."""
	
	def create_order(self, order_type, instrument, side, units, price=0,
		price_bound=0, time_in_force="", stoploss=0, takeprofit=0, own_id="", 
		tag="", comment="", account_id=""):
		"""Create an order for the given instrument with specified parameters.
		
		Args:
			order_type (str):
				Type of order, accepting only value "MARKET", "LIMIT", "STOP" 
				or "MARKET_IF_TOUCHED".
			instrument (str):
				Code of instrument.
			side (str):
				Side of order, accepting only value "BUY" or "SELL".
			units (int):
				Quantity of order.
			price (int, optional):
				Price level for orders "LIMIT", "STOP" and "MARKET_IF_TOUCHED".
			price_bound (int, optional):
				The worse market price that may be filled, goes only for orders 
				"STOP" and "MARKET_IF_TOUCHED".
			time_in_force (str, optional):
				How long should the order remain pending. Accepting only codes 
				"FOK" or "IOC" for the "MARKET" order, for the rest "GTC" or 
				"GTD" or "GFD" codes. "FOK" is default for the "MARKET" type 
				and "GTC" for the waiting types.
			gtd_time (str, optional):
				String represention of an DateTime object in RFC 3339 format.   
			stoploss (int, optional):
				Price where the trade ends around and user losses money.
			trailing_stoploss (int, optional):
				Distance in price units from the triggered price of this order. 
				In the other words, Oanda itself calculcate the difference in 
				pips.
			takeprofit (int, optional):
				Price where the trade ends and user gets profit.
			own_id (str, optional):
				Custom user ID used for this order and if filled, then for the
				open trade.
			tag (str, optional):
				Custom user tag for tagging this order.
			comment (str, optional):
				Custom user comment for this order.
			
		Returns:
			True if the order was created as specified.
			
		Raises:
			HttpError:
				HTTP status code is 4xx or 5xx.
			TypeError:
				Argument for the 'price' parameter is required, if the order 
				type is "LIMIT" or "STOP" or "MARKET_IF_TOUCHED".
			ValueError:
				1. Invalid order type passed to the 'order_type' parameter.
				2. Invalid instrument code passed to the 'instrument' parameter.
				3. Invalid side passes to the 'side' parameter.
				4. Invalid size of units passed to the 'units' parameter.
				5. Invalid TimeInForce code for the given type of order.
				
		TODO:
			- add 'position_fill' parameter if some day a user of this package 
			will want use this option.
		"""
		account_id = account_id or self.default_id
		endpoint = "/{}/orders".format(account_id)
		
		if not order_type in ORDER_TYPE:
			raise ValueError("Invalid order type '{}'.".format(order_type))
		
		if not instrument in INSTRUMENTS.values():
			raise ValueError("Invalid instrument code '{}'.".format(instrument))
		
		if not side in SIDE:
			raise ValueError("Invalid side '{}'.".format(side))
		
		if not units > 0:
			raise ValueError("Invalid size of units '{}'.".format(units))
		
		# Units have to be negative for "SELL" order.
		
		if side == "SELL":
			units = units * -1
		
		if order_type == "MARKET":
			if time_in_force:
				if time_in_force in TIME_IN_FORCE[:2]:
					time_in_force = time_in_force
				else: 
					raise ValueError("Invalid TimeInForce code '{}' for the "
						"'{}' order.".format(time_in_force, order_type)))
			else:
				time_in_force = "FOK"
		elif order_type in ORDER_TYPE[1:]:
			if time_in_force:
				if time_in_force in TIME_IN_FORCE[2:]:
					time_in_force = time_in_force
				else:
					raise ValueError("Invalid TimeInForce code '{}' for the "
						"'{}' order.".format(time_in_force, order_type)))
			else:
				time_in_force = "GTC"
			
			# Argument for the "price" parameter is required for these order
			# types.
			
			if not price:
				raise TypeError("Missing argument for the 'price' parameter "
					"in the '{}' order".format(order_type))
		
		# Content for the POST HTTP method.
		
		body = {
			"order": {
				# Mandatory keys for all order types.
				
				"instrument": instrument,
				"positionFill": "DEFAULT",
				"timeInForce": time_in_force,
				"type": order_type,
				"units": str(units), 
				
				# Voluntary keys (if empty, Oanda will ignore that)
				
				"clientExtensions": {
					"comment": comment,
					"id": str(own_id),
					"tag": tag
				}
			}
		}
		
		# Other voluntary keys which cannot be placed in the "body" variable 
		# if they are empty, otherwise Oanda raises error messages for them. 
		
		if price:
			body["order"].update({"price": str(price)})
		
		if price_bound:
			body["order"].update({"priceBound": str(price_bound)})
		
		if stoploss:
			body["order"].update({
				"stopLossOnFill": {
					"price": str(stoploss),
					"timeInForce": "GTC"
				}
			})
		
		if trailing_stoploss:
			body["order"].update({
				"trailingStopLossOnFill": {
					"distance": str(trailing_stoploss),
					"timeInForce": "GTC"
				}
			})
			
		if takeprofit:
			body["order"].update({
				"takeProfitOnFill": {
					"price": str(takeprofit),
					"timeInForce": "GTC"
				}
			})
		
		response = self.send_request(endpoint, "POST", json=body)
		
		if response.status_code >= 400:
			response.raise_for_error()
	
		return response.status_code == 201
		
	def get_order_details(self, order_id=0, own_id="", account_id=""):
		"""
		"""
		account_id = account_id or self.default_id
		
		if own_id:
			order_id = "@" + own_id
			
		endpoint = "/{0}/orders/{1}".format(account_id, order_id)
		
		return self.send_request(endpoint)
	
	def get_pending_orders(self, account_id=""):
		account_id = account_id or self.default_id
		endpoint = "/{}/pendingOrders".format(account_id)
		
		return self.send_request(endpoint)
	
	def modify_pending_order(self, order_id=0, own_id="", price=0,
			price_bound=0, units=0, stoploss=0, takeprofit=0, new_own_id="", 
			tag="", comment="", account_id=""):
		"""User may use custom ID via '@value'"""
		account_id = account_id or self.default_id
		
		if own_id:
			order_id = "@" + own_id
			
		endpoint = "/{0}/orders/{1}".format(account_id, order_id)
		
		# 
		
		order_detail = (
			self.get_order_details(order_id, account_id=account_id)
				.json()["order"]
		)
		
		# Remove unwanted Oanda in-house keys from order_detail
		
		unwanted_keys = [
			"createTime", "id", "partialFill", "state", "triggerCondition"
		]
		
		for key in unwanted_keys:
			order_detail.pop(key)
			
		# Change value for key "positionFill" to "DEFAULT" because Oanda
		# has changed internally the value for their purposes
		
		order_detail["positionFill"] = "DEFAULT"
		
		# Update values as a user demands (eg. change stoploss price)
		
		if price:
			order_detail["price"] = str(price)
		
		if price_bound:
			order_detail["priceBound"] = str(price_bound)
		
		if units:
			order_detail["units"] = str(units)
		
		if stoploss:
			order_detail["stopLossOnFill"]["price"] = str(stoploss)
			
		if takeprofit:
			order_detail["stopLossOnFill"]["price"] = str(stoploss)
		
		if new_own_id:
			order_detail["clientExtensions"]["id"] = new_own_id
		
		if tag:
			order_detail["clientExtensions"]["tag"] = tag
		
		if comment:
			order_detail["clientExtensions"]["comment"] = comment
		
		order = {"order": order_detail}
		
		return self.send_request(endpoint, "PUT", json=order)
		
	def cancel_pending_order(self, order_id, account_id=""):
		account_id = account_id or self.default_id
		endpoint = "/{0}/orders/{1}/cancel".format(account_id, order_id)
		
		return self.send_request(endpoint, "PUT")
	
	def cancel_all_pending_orders(self):
		"""use async
		default all, if insturment, then only for given instrumet
		"""
		pass
