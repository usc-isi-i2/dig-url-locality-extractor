# -*- coding: utf-8 -*-
import copy 
import types
from digExtractor.extractor import Extractor
from digDictionaryExtractor.populate_trie import populate_trie
import url_helper

class UrlExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['url']
        self.cities = None
        self.states = None
        self.countries_dict = {}
        self.countries = None
        self.stop_words = None

    def get_cities(self):
        return self.cities

    def set_cities(self, cities):
        if not isinstance(cities, list):
            raise ValueError("cities must be a list")
        self.cities = populate_trie(iter(cities))
        return self

    def get_states(self):
        return self.states

    def set_states(self, states):
        if not isinstance(states, list):
            raise ValueError("states must be a list")
        self.states = populate_trie(iter(states))
        return self

    def get_countries_dict(self):
        return self.countries_dict

    def set_country_code_to_country(self, country_code_to_country):
        if not isinstance(country_code_to_country, dict):
            raise ValueError("country_code_to_country must be a dict")
        self.countries_dict = country_code_to_country
        countries_val = [x.lower() for x in country_code_to_country.values()]
        self.countries = populate_trie(iter(countries_val))
        return self

    def get_stop_words(self):
        return self.stop_words

    def set_stop_words(self, stop_words):
        if not isinstance(stop_words, list):
            raise ValueError("stop_words must be a list")
        self.stop_words = populate_trie(iter(stop_words))
        return self
        
    def extract(self, doc):
        if 'url' in doc:
            return url_helper.extract(doc['url'], self.cities, self.states, self.countries_dict, self.countries, self.stop_words)
        return None

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields