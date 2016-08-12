from typing import List, Union

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


class AccountMixin:
    """Methods in the AccountMixin class handles the account endpoints."""

    def get_available_accounts(self) -> dict:
        """Get list of accounts for the current access token.

        Returns:
            JSON object (dict) with the accounts IDs.

        Example:
            {
                "accounts": [
                    {
                        "id": "<ACCOUNT ID>",
                        "tags": []
                    },
                    {
                        ...
                    }
                ]
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        endpoint = ""
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_account(self, account_id: str = "") -> dict:
        """Get full account details.

        This option includes information about pending orders, open trades and
        closed positions.

        Arguments:
            account_id:
                Oanda trading account ID, otherwise 'default_id' will be used.

        Returns:
            JSON object (dict) with the full account details.

        Example:
            {
                "account": {
                    "NAV": "43650.78835",
                    "alias": "My New Account #2",
                    "balance": "43650.78835",
                    "createdByUserID": <USERID>,
                    "createdTime": "2015-08-12T18:21:00.697504698Z",
                    "currency": "CHF",
                    "hedgingEnabled": false,
                    "id": "<ACCOUNT>",
                    "lastTransactionID": "6356",
                    "marginAvailable": "43650.78835",
                    "marginCloseoutMarginUsed": "0.00000",
                    "marginCloseoutNAV": "43650.78835",
                    "marginCloseoutPercent": "0.00000",
                    "marginCloseoutPositionValue": "0.00000",
                    "marginCloseoutUnrealizedPL": "0.00000",
                    "marginRate": "0.02",
                    "marginUsed": "0.00000",
                    "openPositionCount": 0,
                    "openTradeCount": 0,
                    "orders": [],
                    "pendingOrderCount": 0,
                    "pl": "-56034.41199",
                    "positionValue": "0.00000",
                    "positions": [
                        {
                            "instrument": "EUR_GBP",
                            "long": {
                                "pl": "-21.81721",
                                "resettablePL": "-21.81721",
                                "units": "0",
                                "unrealizedPL": "0.00000"
                            },
                            "pl": "-21.81721",
                            "resettablePL": "-21.81721",
                            "short": {
                                "pl": "0.00000",
                                "resettablePL": "0.00000",
                                "units": "0",
                                "unrealizedPL": "0.00000"
                            },
                            "unrealizedPL": "0.00000"
                        },
                        {
                            ...
                        }
                    ],
                    "resettablePL": "-56034.41199",
                    "trades": [],
                    "unrealizedPL": "0.00000",
                    "withdrawalLimit": "43650.78835"
                },
                "lastTransactionID": "6356"
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_account_summary(self, account_id: str = "") -> dict:
        """Get short variant of account details.

        In this option are excluded pendings orders, open trades, closed
        positions.

        Arguments:
            account_id:
                Oanda trading account ID, otherwise 'default_id' will be used.

        Returns:
            JSON object (dict) with the account summary details.

        Example:
            {
                "account": {
                    "NAV": "43650.78835",
                    "alias": "My New Account #2",
                    "balance": "43650.78835",
                    "createdByUserID": <USERID>,
                    "createdTime": "2015-08-12T18:21:00.697504698Z",
                    "currency": "CHF",
                    "hedgingEnabled": false,
                    "id": "<ACCOUNT>",
                    "lastTransactionID": "6356",
                    "marginAvailable": "43650.78835",
                    "marginCloseoutMarginUsed": "0.00000",
                    "marginCloseoutNAV": "43650.78835",
                    "marginCloseoutPercent": "0.00000",
                    "marginCloseoutPositionValue": "0.00000",
                    "marginCloseoutUnrealizedPL": "0.00000",
                    "marginRate": "0.02",
                    "marginUsed": "0.00000",
                    "openPositionCount": 0,
                    "openTradeCount": 0,
                    "pendingOrderCount": 0,
                    "pl": "-56034.41199",
                    "positionValue": "0.00000",
                    "resettablePL": "-56034.41199",
                    "unrealizedPL": "0.00000",
                    "withdrawalLimit": "43650.78835"
                },
                "lastTransactionID": "6356"
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/summary".format(account_id)
        response = self.send_request(endpoint)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def get_instruments(self, instruments: List[str] = [],
                        account_id: str = "") \
            -> dict:
        """Get details for one or more or all tradeable instruments.

        If a user won't pass any instrument code(s) to the 'instruments'
        parameter, then will be returned details for all instruments.

        Arguments:
            instruments:
                Code of instrument(s).
            account_id (str):
                Oanda trading account ID, otherwise 'default_id' will be used.

        Returns:
            JSON object (dict) with the instrument(s) details.

        Example:
            {
                "instruments": [
                    {
                        "displayName": "USD/THB",
                        "displayPrecision": 3,
                        "marginRate": "0.05",
                        "maximumOrderUnits": "100000000",
                        "maximumPositionSize": "0",
                        "maximumTrailingStopDistance": "100.000",
                        "minimumTradeSize": "1",
                        "minimumTrailingStopDistance": "0.050",
                        "name": "USD_THB",
                        "pipLocation": -2,
                        "tradeUnitsPrecision": 0,
                        "type": "CURRENCY"
                    },
                    {
                        ...
                    }
                ]
            }

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid instrument code(s) passed to the 'instruments'
                parameter.
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/instruments".format(account_id)

        if instruments:
            for code in instruments:
                if code in INSTRUMENTS.values():
                    continue
                else:
                    raise ValueError("Invalid instrument code '{}'".format(
                        code))

        url_params = {"instruments": ",".join(instruments)}
        response = self.send_request(endpoint, params=url_params)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.json()

    def configure_account(self, margin: Union[float, int],
                          account_id: str = "") \
            -> bool:
        """Configure the given trading account.

        By this method is possible only configure margin rate alias minimum
        required margin per trade. Allowed values are below in the 'Minimum
        margin' column (without the percentage sign).

        | Leverage ratio | Minimum margin | Margin rate |
        | --- | --- | --- |
        | 100:1 | 1 % | 0.01 |
        | 50:1 | 2 % | 0.02 |
        | 40:1 | 2.5 % | 0.025 |
        | 30:1 | 3.3 % | 0.0333 |
        | 20:1 | 5 % | 0.05 |
        | 10:1 | 10 % | 0.1 |

        Arguments:
            margin:
                Minimum margin per trade expressed in the percentage.

        Returns:
            True if the account was configured successfully.

        Raises:
            requests.HTTPError:
                HTTP response status code is 4xx or 5xx.
            ValueError:
                Invalid
        """
        account_id = account_id or self.default_id
        endpoint = "/{}/configuration".format(account_id)
        margin_rate = {
            1: 0.01,
            2: 0.02,
            2.5: 0.025,
            3.3: 0.0333,
            5: 0.05,
            10: 0.1
        }

        if margin not in margin_rate.keys():
            raise ValueError("Invalid margin '{} %'.".format(margin))

        request_body = {"marginRate": str(margin_rate[margin])}
        response = self.send_request(endpoint, "PATCH", json=request_body)

        if response.status_code >= 400:
            response.raise_for_status()

        return response.status_code == 200
