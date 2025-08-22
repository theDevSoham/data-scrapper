from SocialMediaScrapper import FacebookScrapper, TwitterScrapper, InstagramScrapper
from utils import Parser, Normalizer, StorageGateway
from Orchestrator import Orchestrator


if __name__ == "__main__":
    parser = Parser()
    normalizer = Normalizer()
    storage = StorageGateway()

    instagram_scrapper = InstagramScrapper("Insta token")
    facebook_scrapper = FacebookScrapper("Facebook token")
    twitter_scrapper = TwitterScrapper("Twiitter token")
    orchestrator = Orchestrator.Orchestrator(
        scrappers=[instagram_scrapper, facebook_scrapper, twitter_scrapper],
        parser=parser,
        normalizer=normalizer,
        storage_gateway=storage
    )

    orchestrator.run()
