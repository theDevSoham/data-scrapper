from SocialMediaScrapper import FacebookScrapper, TwitterScrapper, InstagramScrapper
from utils import Parser, Normalizer, StorageGateway
from Orchestrator import Orchestrator


if __name__ == "__main__":
    parser = Parser()
    normalizer = Normalizer()
    storage = StorageGateway()

    instagram_scrapper = InstagramScrapper("Insta token")
    # facebook_scrapper = FacebookScrapper("Facebook token")
    twitter_scrapper = TwitterScrapper("RHM1dENLTDF3MGJZdXhZSy1XZi1LVF9NVi1KU2RwdlRsM1NpWVp5eWtUdnUyOjE3NTY0ODE3NzI0ODI6MTowOmF0OjE")
    orchestrator = Orchestrator.Orchestrator(
        scrappers=[
            instagram_scrapper, 
            # facebook_scrapper, 
            twitter_scrapper
        ],
        parser=parser,
        normalizer=normalizer,
        storage_gateway=storage
    )

    orchestrator.run()
