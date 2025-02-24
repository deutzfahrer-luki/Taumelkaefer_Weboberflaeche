import json

DEFAULT_PFAD = "config.json"

class ConfigLoader:
    def __init__(self, filename=DEFAULT_PFAD):
        self.filename = filename
        self.data = self._load_config()

    def _load_config(self):
        # Lädt die JSON-Datei und gibt sie als Dictionary zurück.
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
        # Gibt einen Wert aus der Konfiguration zurück.
        return self.data.get(key, default)

if __name__ == "__main__":
    config = ConfigLoader()
    print(config.get("ip"))
