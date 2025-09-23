class AuthenticationError(Exception):
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)
        

class ScraperError(Exception):
    def __init__(self, message="Scraping failed"):
        self.message = message
        super().__init__(self.message)        