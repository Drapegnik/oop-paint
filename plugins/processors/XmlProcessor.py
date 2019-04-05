import json
from dicttoxml import dicttoxml
from xmltodict import parse

from core.processing import FileProcessor

import pprint

def to_int(items = []):
    return [int(x) for x in items]

def parse_list(xml_list):
    if not xml_list:
        return []
    item = xml_list['item']
    if type(item) == list:
        return list(map(lambda x: to_int(x['item']), item))
    else:
        print(item['item'])
        print()
        return [to_int(item['item'])]


def parse_dict(xml_dict):
    return {
        'name': xml_dict['name'],
        'points': parse_list(xml_dict['points']),
        'data': to_int(xml_dict['data']['item']) if xml_dict['data'] else []
    }


class XmlProcessor(FileProcessor):
    ext = '.xml'
    name = 'XML'

    @staticmethod
    def convert(data):
        return dicttoxml(json.loads(data), custom_root='figures', attr_type=False)

    @staticmethod
    def parse(xml):
        figures = json.loads(json.dumps(parse(xml)))['figures']['item']
        figures = parse(xml)['figures']['item']
        return json.dumps(list(map(parse_dict, figures)))
