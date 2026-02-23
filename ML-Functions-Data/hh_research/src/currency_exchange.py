
import json
from typing import Dict

import requests


class Exchanger:
    __EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/RUB"

    def __init__(self, config_path: str):
        self.config_path = config_path

    def update_exchange_rates(self, rates: Dict):
       

        try:
            response = requests.get(self.__EXCHANGE_URL)
            new_rates = response.json()["rates"]
        except requests.exceptions.SSLError:
            raise AssertionError("[FAIL] Cannot get exchange rate! Try later or change the host API")

        for curr in rates:
            rates[curr] = new_rates[curr]

        # Change 'RUB' to 'RUR'
        rates["RUR"] = rates.pop("RUB")

    def save_rates(self, rates: Dict):
        """Save rates to JSON config."""

        with open(self.config_path, "r") as cfg:
            data = json.load(cfg)

        data["rates"] = rates

        with open(self.config_path, "w") as cfg:
            json.dump(data, cfg, indent=2)


if __name__ == "__main__":
    _exchanger = Exchanger("../settings.json")
    _default = {"RUB": None, "USD": None, "EUR": None, "UAH": None}
    _exchanger.update_exchange_rates(_default)
    _exchanger.save_rates(_default)
    for _k, _v in _default.items():
        print(f"{_k}: {_v :.05f}")
