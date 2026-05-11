import json


class PerformanceData:

    path_to_perf_file = "\\pages\\radar\\data\\aircraft_performance.json"

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.load_perf_file()
        self.data = {}

    def load_perf_file(self):
        file = self.root_dir + self.path_to_perf_file
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)
            for item in data:
                pass

    def get_wtc(self, icao_type):
        return "M"