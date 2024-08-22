import json
from pathlib import Path
import shutil


class PerformanceSettings:
    DEFAULT_PERFORMANCE_FILE = Path("settings/performance.default")
    PERFORMANCE_FILE = Path("settings/performance.json")
    CUSTOM_PERFORMANCE = "Custom..."

    default_settings = {
        "custom_steps": 30,
        "cfg": 8,
        "sampler_name": "dpmpp_2m_sde_gpu",
        "scheduler": "karras",
        "clip_skip": 1,
    }

    def __init__(self):
        self.performance_options = self.load_performance()

    def load_performance(self):
        default_data = self._load_data(self.DEFAULT_PERFORMANCE_FILE)
        data = self._load_data(self.PERFORMANCE_FILE)

        for name, default_settings in default_data.items():
            if name not in data:
                data[name] = default_settings
            else:
                existing_settings = data[name]
                merged_settings = existing_settings | default_settings
                data[name] = merged_settings

        self._save_data(self.PERFORMANCE_FILE, data)
        return data

    def _load_data(self, file_path):
        if not file_path.exists():
            shutil.copy(self.DEFAULT_PERFORMANCE_FILE, file_path)
        return json.load(open(file_path))

    def _save_data(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def save_performance(self, perf_options):
        with open(self.PERFORMANCE_FILE, "w") as f:
            json.dump(perf_options, f, indent=2)
        self.performance_options = self.load_performance()

    def get_perf_options(self, name):
        return self.performance_options[name]
