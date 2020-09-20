import logging
import requests
import traceback
import json
import xmltodict
import sys
import argparse


class GoodreadsAPIClient(object):
    KEY = "5VI9EeBQZ7z2P7SadUXFvQ"

    def __init__(self, url):
        self.url = url + "?format=xml&key={}".format(self.KEY)

    @staticmethod
    def _get_title(response_data):
        try:
            return response_data['book']['title']
        except KeyError:
            pass

    @staticmethod
    def _get_average_rating(response_data):
        try:
            return response_data['book']['average_rating']
        except KeyError:
            pass

    @staticmethod
    def _get_num_pages(response_data):
        try:
            return response_data['book']['num_pages']
        except KeyError:
            pass

    @staticmethod
    def _get_image_url(response_data):
        try:
            return response_data['book']['image_url']
        except KeyError:
            pass

    @staticmethod
    def _get_publication_year(response_data):
        try:
            return response_data['book']['work']['original_publication_year']['#text']
        except KeyError:
            pass

    @staticmethod
    def _get_authors(response_data):
        try:

            if isinstance(response_data['book']['authors']['author'], list):

                return ",".join([response_data['book']['authors']['author'][author]["name"] for author in
                                 range(len(response_data['book']['authors']['author']))])

            else:
                return response_data['book']['authors']['author']["name"]

        except KeyError:
            pass

    def get_book_details(self):

        try:
            # GET response
            response_data = requests.get(self.url)
            # initialize dict
            book_details = dict()
            response_data.raise_for_status()
            if response_data.status_code == 200:

                # parse response to dict
                response_dict = xmltodict.parse(response_data.content)
                book_details["title"] = self._get_title(response_dict['GoodreadsResponse'])
                book_details["ratings_count"] = self._get_average_rating(response_dict['GoodreadsResponse'])
                book_details["num_pages"] = self._get_num_pages(response_dict['GoodreadsResponse'])
                book_details["image_url"] = self._get_image_url(response_dict['GoodreadsResponse'])
                book_details["publication_year"] = self._get_publication_year(response_dict['GoodreadsResponse'])
                book_details["authors"] = self._get_authors(response_dict['GoodreadsResponse'])

            else:
                book_details = {}

            return json.dump(book_details, sys.stdout, indent=4)

        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error(e)
            return "raise an exception InvalidGoodreadsURL"


if __name__ == "__main__":
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-url", "--GoodreadUrl", required=True, help="Goodreads URL string as input")
    args = vars(ap.parse_args())

    GoodReads = GoodreadsAPIClient(args['GoodreadUrl'])
    GoodRead = GoodReads.get_book_details
