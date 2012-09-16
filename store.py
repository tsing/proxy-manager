import ConfigParser

class Store:
    def __init__(self):
        self.domains = self.load_domains()

    def load_domains(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')
        return self.config.items('domains') 

    def index(self):
        return self.domains

    def delete(self, domain):
        self.config.remove_option('domains', domain)
        return self.save()

    def get(self, domain):
        return self.config.get('domains', domain)

    def create(self, domain):
        self.config.set('domains', domain, 1)
        return self.save()

    def save(self):
        with open('config.ini', 'w') as configfile:
            return self.config.write(configfile)
