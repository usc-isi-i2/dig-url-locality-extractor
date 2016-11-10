import sys
import time
import os
import json
import codecs
import unittest

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digUrlLocalityExtractor.url_extractor import UrlExtractor

class TestCityExtractorMethods(unittest.TestCase):

    def load_file(self, filename):
        names_file = os.path.join(os.path.dirname(__file__), filename)
        names = json.load(codecs.open(names_file, 'r', 'utf-8'))
        return names

    def test_url_extractor(self):
        doc = {"url": "https://247gfe.com/escort-locations/irelanddublintranssexual-escorts/"}
        cities = self.load_file("cities.json")
        add_cities = self.load_file("add_cities_for_url.json")
        cities.extend(add_cities)
        states = self.load_file("states.json")
        country_dict = self.load_file("country_codes_dict.json")
        stop_words = self.load_file("stop_words.json")
        extractor = UrlExtractor().set_cities(cities).set_metadata({'extractor': 'url'}).set_states(states).set_country_code_to_country(country_dict).set_stop_words(stop_words)
        extractor_processor = ExtractorProcessor().set_input_fields(['url']).set_output_field('url_locality').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['url_locality'][0]['value'], {"cities": ["dublin"], "states": [], "countries": ["ireland"]})


if __name__ == '__main__':
    unittest.main()



