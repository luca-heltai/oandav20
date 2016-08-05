from .account import INSTRUMENTS


class PricingMixin(object):
    """Methods in the PricingMixin class handles the pricing endpoints."""
        
    def get_pricing_info(self, instruments):
        """Get pricing information for 1 or more instruments.
        
        Arguments:
            instruments (list):
                Code of instrument(s).
        
        Note:
            Even if instrument code(s) are invalid, Oanda responds with HTTP 
            status 200 and normal JSON Pricing object, however details won't be 
            provided and thus an instrument code control is needed.
    
        Returns:
            JSON object with the pricing information.
        
        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid instrument code passed to the 'instruments' 
                parameter.
        """
        account_id = self.default_id
        endpoint = "/{}/pricing".format(account_id)
        
        for code in instruments:
            if code in INSTRUMENTS.values():
                continue
            else:
                raise ValueError("Invalid instrument code '{}'.".format(code))
            
        url_params = {"instruments": ",".join(instruments)}
        response = self.send_request(endpoint, params=url_params)
        
        if response.status_code >= 400:
            response.raise_for_status()
    
        return response.json()
