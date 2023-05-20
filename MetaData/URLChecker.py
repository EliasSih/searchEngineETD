import os
import requests
from lxml import etree

def send_get_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f'Error sending GET request to {url}: {str(e)}')
        return False

def main(directory):
    for filename in os.listdir(directory):
        print("filename:", filename)
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(file_path, parser)
            root = tree.getroot()

            for doc in root.iter('doc'):
                for field in doc.iter('field'):
                    if field.attrib.get('name') == 'identifier':
                        url = field.text
                        if send_get_request(url):
                            ranking = etree.SubElement(doc, 'field')
                            ranking.attrib['name'] = 'ranking'
                            ranking.text = '5'

            # Write the changes back to the file
            with open(file_path, 'wb') as file:
                tree.write(file, pretty_print=True, xml_declaration=True, encoding='utf-8')

if __name__ == "__main__":
    directory = 'MetaData/TestDir'  # replace with your directory
    main(directory)