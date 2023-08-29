import csv
import xml.etree.ElementTree
import json


def read_csv_data(file):
    csv_reader = csv.reader(file)
    data = [" ".join(row) for row in csv_reader]
    return "\n".join(data)


def parse_xml(file_path):
    tree = xml.etree.ElementTree.parse(file_path)
    root = tree.getroot()

    def element_to_dict(element):
        data = {}
        for child in element:
            if list(child):
                data[child.tag] = element_to_dict(child)
            else:
                data[child.tag] = child.text
        return data

    xml_dict = element_to_dict(root)
    return json.dumps(xml_dict, indent=4)
