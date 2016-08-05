class TradesMixin:
    """Methods in the TradesMixin class handles the trades endpoints."""
    
    def get_open_trades(self, account_id=""):
        """Get list of all open trades.
        
        Arguments:
            account_id (str, optional):
                Oanda account ID.
        
        Returns:
            JSON object with the open trades details.
        
        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/openTrades".format(account_id)
        
        response = self.send_request(endpoint)
        
        if response.status_code >= 400:
            response.raise_for_status()
    
        return response.json()
    
    def get_trade_details(self, trade_id=0, own_id="", account_id=""):
        """Get details for the given trade.
        
        Arguments:
            trade_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optinal):
                Custom trade ID.
            account_id (str, optional):
                Oanda account ID
        
        Returns:
            JSON object with the trade details.

        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
    
    def modify_trade(self):
        pass
    
    def close_trade(self, trade_id=0, own_id="", units=0, account_id=""):
        """Close fully or partially the given open trade.
        
        User may choose if wants to close the trade by Oanda ID or custom ID.
        
        Arguments:
            trade_id (int, optional):
                Trade ID provided by Oanda.
            own_id (str, optional):
                Custom trade ID.
            units (int, optional):
                How many units should be closed. If empty then all units will 
                be used.
            account_id (str, optional):
                Oanda account ID.
            
        Returns:
            True if the trade was closed properly.
            
        Raises:
            HTTPError:
                HTTP response status code is 4xx or 5xx.
            TypeError:
                Missing argument for the 'trade_id' or 'own_id' parameter.
        """
