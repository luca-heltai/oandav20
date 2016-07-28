import requests

from mixins.pricing import PricingMixin

INSTRUMENTS = {
	# Bonds
	
	"Bund": "DE10YB_EUR",
	"UK 10Y Gilt": "UK10YB_GBP",
	"US 10Y T-Note": "USB10Y_USD",
	"US 2Y T-Note": "USB02Y_USD",
	"US 5Y T-Note": "USB05Y_USD",
	"US T-Bond": "USB30Y_USD",
	
	# Commodities
	
	"Brent Crude Oil": "BCO_USD",
	"Corn": "CORN_USD",
	"Natural Gas": "NATGAS_USD",
	"Soybeans": "SOYBN_USD",
	"Sugar": "SUGAR_USD",
	"West Texas Oil": "WTICO_USD",
	"Wheat": "WHEAT_USD",
	
	# Forex
	
	"AUD/CAD": "AUD_CAD",
	"AUD/CHF": "AUD_CHF",
	"AUD/HKD": "AUD_HKD",
	"AUD/JPY": "AUD_JPY",
	"AUD/NZD": "AUD_NZD",
	"AUD/SGD": "AUD_SGD",
	"AUD/USD": "AUD_USD",
	"CAD/CHF": "CAD_CHF",
	"CAD/HKD": "CAD_HKD",
	"CAD/JPY": "CAD_JPY",
	"CAD/SGD": "CAD_SGD",
	"CHF/HKD": "CHF_HKD",
	"CHF/JPY": "CHF_JPY",
	"CHF/ZAR": "CHF_ZAR",
	"EUR/AUD": "EUR_AUD",
	"EUR/CAD": "EUR_CAD",
	"EUR/CHF": "EUR_CHF",
	"EUR/CZK": "EUR_CZK",
	"EUR/DKK": "EUR_DKK",
	"EUR/GBP": "EUR_GBP",
	"EUR/HKD": "EUR_HKD",
	"EUR/HUF": "EUR_HUF",
	"EUR/JPY": "EUR_JPY",
	"EUR/NOK": "EUR_NOK",
	"EUR/NZD": "EUR_NZD",
	"EUR/PLN": "EUR_PLN",
	"EUR/SEK": "EUR_SEK",
	"EUR/SGD": "EUR_SGD",
	"EUR/TRY": "EUR_TRY",
	"EUR/USD": "EUR_USD",
	"EUR/ZAR": "EUR_ZAR",
	"GBP/AUD": "GBP_AUD",
	"GBP/CAD": "GBP_CAD",
	"GBP/CHF": "GBP_CHF",
	"GBP/HKD": "GBP_HKD",
	"GBP/JPY": "GBP_JPY",
	"GBP/NZD": "GBP_NZD",
	"GBP/PLN": "GBP_PLN",
	"GBP/SGD": "GBP_SGD",
	"GBP/USD": "GBP_USD",
	"GBP/ZAR": "GBP_ZAR",
	"HKD/JPY": "HKD_JPY",
	"NZD/CAD": "NZD_CAD",
	"NZD/CHF": "NZD_CHF",
	"NZD/HKD": "NZD_HKD",
	"NZD/JPY": "NZD_JPY",
	"NZD/SGD": "NZD_SGD",
	"NZD/USD": "NZD_USD",
	"SGD/CHF": "SGD_CHF",
	"SGD/HKD": "SGD_HKD",
	"SGD/JPY": "SGD_JPY",
	"TRY/JPY": "TRY_JPY",
	"USD/CAD": "USD_CAD",
	"USD/CHF": "USD_CHF",
	"USD/CNH": "USD_CNH",
	"USD/CZK": "USD_CZK",
	"USD/DKK": "USD_DKK",
	"USD/HKD": "USD_HKD",
	"USD/HUF": "USD_HUF",
	"USD/INR": "USD_INR",
	"USD/JPY": "USD_JPY",
	"USD/MXN": "USD_MXN",
	"USD/NOK": "USD_NOK",
	"USD/PLN": "USD_PLN",
	"USD/SAR": "USD_SAR",
	"USD/SEK": "USD_SEK",
	"USD/SGD": "USD_SGD",
	"USD/THB": "USD_THB",
	"USD/TRY": "USD_TRY",
	"USD/ZAR": "USD_ZAR",
	"ZAR/JPY": "ZAR_JPY",
	
	# Indices
	
	"Australia 200": "AU200_AUD",
	"Europe 50": "EU50_EUR",
	"France 40": "FR40_EUR",
	"Germany 30": "DE30_EUR",
	"Hong Kong 33": "HK33_HKD",
	"Japan 255": "JP225_USD",
	"Netherlands 25": "NL25_EUR",
	"Singapore 30": "SG30_SGD",
	"Swiss 20": "CH20_CHF",
	"UK 100": "UK100_GBP",
	"US Nas 100": "NAS100_USD",
	"US Russ 2000": "US2000_USD",
	"US SPX 500": "SPX500_USD",
	"US Wall St 30": "US30_USD",
	
	# Metals
	
	"Copper": "XCU_USD",
	"Gold": "XAU_USD",
	"Gold/AUD": "XAU_AUD",
	"Gold/CAD": "XAU_CAD",
	"Gold/CHF": "XAU_CHF",
	"Gold/EUR": "XAU_EUR",
	"Gold/GBP": "XAU_GBP",
	"Gold/HKD": "XAU_HKD",
	"Gold/JPY": "XAU_JPY",
	"Gold/NZD": "XAU_NZD",
	"Gold/SGD": "XAU_SGD",
	"Gold/Silver": "XAU_XAG",
	"Palladium": "XPD_USD",
	"Platinum": "XPT_USD",
	"Silver": "XAG_USD",
	"Silver/AUD": "XAG_AUD",
	"Silver/CAD": "XAG_CAD",
	"Silver/CHF": "XAG_CHF",
	"Silver/EUR": "XAG_EUR",
	"Silver/GBP": "XAG_GBP",
	"Silver/HKD": "XAG_HKD",
	"Silver/JPY": "XAG_JPY",
	"Silver/NZD": "XAG_NZD",
	"Silver/SGD": "XAG_SGD"
}


class Oanda(PricingMixin):
	"""Oanda is the only (main) class, which should be used by user.
	
	It consist of several inherited mixins which extends funcionality of
	this class. Each mixin covers a thematic endpoints, eg. one for orders
	handling, another for getting account information etc.
	
	Attrs:
		__base_url (str): A prefix for all endpoints
		__client (object): An session object with an HTTP persistent
			connection to the Oanda API server.
		default_id (str): An default account ID used for constructing a URL 
			path. If a user manages more accounts, then in each method
			(where necessary) he / she has to provide appropriate ID
	"""
	
	def __init__(self, environment, access_token, default_id):
		"""Initialize an Oanda instance.
		
		Args:
			environment (str): Accept only "demo" or "real"
			access_token (str): An access token for user authentication
		
		Raises:
			ValueError: "demo" or "real" wasn't passed to 'environment'
				parameter
		"""
		if environment == "demo":
			self.__base_url = "https://api-fxpractice.oanda.com/v3/accounts"
		elif environment == "real":
			self.__base_url = "https://api-fxtrade.oanda.com/v3/accounts"
		else:
			raise ValueError("Invalid argument passed to 'environment' "
				"parameter")

		self.__client = requests.Session()
		self.__client.headers["Authorization"] = "Bearer " + access_token
		self.__client.headers["Content-Type"] = "application/json"
		
		self.default_id = default_id
		
	def send_request(self, endpoint, method="GET", **kwargs):
		"""Send an HTTP request to the Oanda server.
		
		A user may also use this method for accessing another endpoints which
		aren't covered in this package.
		
		Args:
			endpoint (str): A suffix of a URL.
			method (str, optional): A HTTP method written in capital letters.
			**kwargs: Same keywords arguments like for 'request' object in
				'requests' package.					
			 
		"""
		url = self.__base_url + endpoint
		
		return self.__client.request(method, url, **kwargs)
