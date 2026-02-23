import os
from typing import Optional

from src.analyzer import Analyzer
from src.currency_exchange import Exchanger
from src.data_collector import DataCollector
from src.parser import Settings
from src.predictor import Predictor

CACHE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cache")
SETTINGS_PATH = "settings.json"


class ResearcherHH:
   

    def __init__(self, config_path: str = SETTINGS_PATH, no_parse: bool = False):
        self.settings = Settings(config_path, no_parse=no_parse)
        self.exchanger = Exchanger(config_path)
        self.collector: Optional[DataCollector] = None
        self.analyzer: Optional[Analyzer] = None
        self.predictor = Predictor()

    def update(self, **kwargs):
        self.settings.update_params(**kwargs)
        if not any(self.settings.rates.values()) or self.settings.update:
            print("[INFO]: Trying to get exchange rates from remote server...")
            self.exchanger.update_exchange_rates(self.settings.rates)
            self.exchanger.save_rates(self.settings.rates)

       
        self.collector = DataCollector(self.settings.rates)
        self.analyzer = Analyzer(self.settings.save_result)

    def __call__(self):
        
        vacancies = self.collector.collect_vacancies(
            query=self.settings.options, refresh=self.settings.refresh, num_workers=self.settings.num_workers
        )
        #print(vacancies)
        #print("[INFO]: Prepare dataframe...")
        df = self.analyzer.prepare_df(vacancies)
        #print("\n[INFO]: Analyze dataframe...")
        self.analyzer.analyze_df(df)
        #print("\n[INFO]: Predict None salaries...")
        #total_df = self.predictor.predict(df)
        #self.predictor.plot_results(total_df)
        #print("[INFO]: Done! Exit()")
        df.to_csv('new13.csv', index=False)


if __name__ == "__main__":
    hh_analyzer = ResearcherHH()
    hh_analyzer.update()
    hh_analyzer()
