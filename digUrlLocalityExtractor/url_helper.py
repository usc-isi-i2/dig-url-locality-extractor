# -*- coding: utf-8 -*-
import json
import string
import pygtrie as trie
from digDictionaryExtractor.populate_trie import populate_trie
from digDictionaryExtractor.name_dictionary_extractor import get_name_dictionary_extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digCrfTokenizer.crf_tokenizer import CrfTokenizer

# Words to reduce tokens
other_words = ['http', 'www', 'co', 'ad', '.', '/', '-', ':', '_', '+', '?', ',' 'com', 'escort', 'escorts', 'https']

def tokenize(raw):
    t = CrfTokenizer()
    t.setRecognizeHtmlEntities(True)
    t.setRecognizeHtmlTags(True)
    t.setSkipHtmlTags(True)
    t.setRecognizePunctuation(True)
    tokens = t.tokenize(raw)
    return tokens

def extract(doc, cities, states, countries_dict, countries, stop_words):
    url = doc
    tokens_doc = tokenize(doc)
    tokens_doc = [x for x in tokens_doc if x not in other_words]
    doc = {'text': tokens_doc}
    dict_out = {}

    #Get cities from tokens    
    e = get_name_dictionary_extractor(cities).set_pre_filter(lambda x:x).set_pre_process(lambda x:x.lower())
    e.set_ngrams(3)
    e.set_joiner(' ')
    ep = ExtractorProcessor().set_input_fields('text').set_output_field('cities').set_extractor(e)
    updated_doc = ep.extract(doc)
    try:
        #Hack for kansas city (kc) as it appears a lot and is specfic to only this case
        value = updated_doc['cities'][0]['value']
        if 'kc' in value:
            value.append('kansas city')
        dict_out['cities'] = [x for x in value if len(x) > 3 and x not in stop_words]
    except Exception:
        dict_out['cities'] = []

    #Get states from tokens
    e = get_name_dictionary_extractor(states).set_pre_filter(lambda x:x).set_pre_process(lambda x:x.lower())
    e.set_ngrams(3)
    e.set_joiner(' ')
    ep = ExtractorProcessor().set_input_fields('text').set_output_field('states').set_extractor(e)
    updated_doc = ep.extract(doc)
    try:
        dict_out['states'] = [x for x in updated_doc['states'][0]['value'] if x not in stop_words]
    except Exception:
        dict_out['states'] = []

    #Get countries from tokens
    e = get_name_dictionary_extractor(countries).set_pre_filter(lambda x:x).set_pre_process(lambda x:x.lower())
    e.set_ngrams(3)
    e.set_joiner(' ')
    ep = ExtractorProcessor().set_input_fields('text').set_output_field('countries').set_extractor(e)
    updated_doc = ep.extract(doc)
    try:
        dict_out['countries'] = [x for x in updated_doc['countries'][0]['value'] if x not in stop_words]
    except Exception:
        dict_out['countries'] = []

    #Get country codes from url
    ann_countries = []
    for token in tokens_doc:
        if token in countries_dict:
            #Check if its actually a country code in the orig url
            pos = url.find(token)
            if url[pos-3:pos] in ['co.', 'ac.'] or url[pos-4:pos] in ['org.', 'com.', 'edu.', 'gov.']:
                ann_countries.append(countries_dict[token])
    dict_out['countries'].extend(ann_countries)

    for token in tokens_doc:
        for i in range(0, len(token)):
            for j in range(i):
                #Cities
                value = token[j:i]
                city = cities.get(value)
                if city is not None and len(value) > 4 and value not in stop_words:
                    dict_out['cities'].append(value)
                #States
                state = states.get(value)
                if state is not None and len(value) > 4 and value not in stop_words:
                    dict_out['states'].append(value)

                #Countries
                country = countries.get(value)
                if country is not None and len(value) > 4 and value not in stop_words:
                    dict_out['countries'].append(value)

    return dict_out
