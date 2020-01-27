import yaml


class Settings:
    def __init__(self):
        with open('settings.yml') as f:
            settings = yaml.safe_load(f)
            self.user = settings['user']
            self.imap_server = settings['imap_server']
