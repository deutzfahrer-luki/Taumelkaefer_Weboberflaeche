import json

DEFAULT_PFAD = "config.json"

class ConfigLoader:
    def __init__(self, filename=DEFAULT_PFAD):
        self.filename = filename
        self.data = self._load_config()

    def _load_config(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Datei {self.filename} nicht gefunden!")
            return {}
        except json.JSONDecodeError:
            print(f"Fehler beim Parsen von {self.filename}!")
            return {}

    def get(self, key, default=None):
        return self.data.get(key, default)
    
    # def save_to_js(self, js_filename="config.js"):
    #     ip = self.get("ip", "127.0.0.1")
    #     js_content = f'const IP_ADDRESS = "{ip}";\nexport default IP_ADDRESS;'

    #     try:
    #         with open(js_filename, "w") as js_file:
    #             js_file.write(js_content)
    #         print(f"{js_filename} wurde erfolgreich erstellt.")
    #     except Exception as e:
    #         print(f"Fehler beim Schreiben der JS-Datei: {e}")
