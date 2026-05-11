import json


class PerformanceData:

    path_to_perf_file = "\\pages\\radar\\data\\aircraft_performance.json"

    def __init__(self, root_dir: str):
        self.wtc_default = "M"
        self.root_dir = root_dir
        self.data = {}
        self.load_perf_file()

    def load_perf_file(self):
        file = self.root_dir + self.path_to_perf_file
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)
            for item in data:
                name = item["ICAO"]
                self.data[name] = {}
                cur = self.data[name]
                cur["WTC"] = item["WTC"]
                cur["ceiling"] = item["ceiling"]
                cur["max_speed"] = item["max_speed"]
                cur["climb"] = []
                cur["descent"] = []
                for rule in item["alt_vars"]:
                    if rule["cr"] == 1:
                        cur["climb"].append({
                            "min": rule["min"],
                            "max": rule["max"],
                            "roc": rule["roc"],
                            "speed": rule["speed"],
                        })
                    elif rule["cr"] == -1:
                        cur["descent"].append({
                            "min": rule["min"],
                            "max": rule["max"],
                            "roc": rule["roc"],
                            "speed": rule["speed"],
                        })

    def get_perf_by_icao(self, icao: str):
        try:
            return self.data[icao]
        except KeyError:
            return False

    def get_wtc(self, icao_type):
        perf = self.get_perf_by_icao(icao_type)
        wtc = self.wtc_default
        try:
            if perf is not False:
                wtc = perf["WTC"]
        except ValueError:
            pass
        else:
            return wtc