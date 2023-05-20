import xml.etree.ElementTree as ET
import re
import requests


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

def parse_xml(xml_file):
    # Parse XML with ElementTree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define namespaces
    namespaces = {
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # Create a list to hold all items
    items = []

    # Iterate over each 'oai_dc:dc' element in the XML
    for metadata in root.findall('.//oai_dc:dc', namespaces):
        # Extract field data
        title = metadata.find('dc:title', namespaces).text if metadata.find('dc:title', namespaces) is not None else None
        creator = metadata.find('dc:creator', namespaces).text if metadata.find('dc:creator', namespaces) is not None else None
        #subject = metadata.find('dc:subject', namespaces).text if metadata.find('dc:subject', namespaces) is not None else None
        description = metadata.find('dc:description', namespaces).text if metadata.find('dc:description', namespaces) is not None else None
        date = metadata.find('dc:date', namespaces).text if metadata.find('dc:date', namespaces) is not None else None
        #identifier = metadata.find('dc:identifier', namespaces).text if metadata.find('dc:identifier', namespaces) is not None else None
        language = metadata.find('dc:language', namespaces).text if metadata.find('dc:language', namespaces) is not None else None
        relation = metadata.find('dc:relation', namespaces).text if metadata.find('dc:relation', namespaces) is not None else None

        count = 0
        subject = []
        for i in metadata.findall('dc:subject', namespaces):
            subject.append(i.text)

        identifier = []
        for i in metadata.findall('dc:identifier', namespaces):
            identifier.append(i.text)

        # Add item data to list
        items.append({
            'title': title,
            'creator': creator,
            'subject': subject,
            'description': description,
            'date': date,
            'identifier': identifier,
            'language': language,
            'relation': relation
        })

    return items


def Extract(xml_file, outputFile):
    items = parse_xml(xml_file)

    # This is the parent (root) tag
    # onto which other tags would be
    # created
    data = ET.Element('add')
    count = 0
    for item in items:
        
        element1 = ET.SubElement(data, 'doc')

        # Adding subtags under the `Opening`
        # subtag
        title = ET.SubElement(element1, 'field')
        creator = ET.SubElement(element1, 'field')
        #subject = ET.SubElement(element1, 'field')
        description = ET.SubElement(element1, 'field')
        date = ET.SubElement(element1, 'field')
        language = ET.SubElement(element1, 'field')
        relation = ET.SubElement(element1, 'field')
        #identifier = ET.SubElement(element1, 'field')

        # Adding attributes to the tags under
        # `items`
        title.set('name', 'title')
        creator.set('name', 'creator')
        #subject.set('name', 'subject')
        description.set('name', 'description')
        date.set('name', 'date')
        language.set('name', 'language')
        relation.set('name', 'relation')
        #identifier.set('name', 'identifier')

        # Adding text between the `E4` and `D5`
        # subtag
        title.text = item["title"]
        creator.text = item["creator"]
        for i in item["subject"]:
            subject = ET.SubElement(element1, 'field')
            subject.set('name', 'subject')
            subject.text = i
        
        #date.text = item["date"]
        if item["date"] is None:
            date.text = "0000"
        elif item["date"] == "<yyyy>" or item["date"] == "n/a":
            date.text = "1111"
        else:
            try:
                date.text = re.search(r"[1-3][0-9]{3}", item["date"]).group(0)
            #print(item["title"],date.text)
            #print(re.search(r"[1-3][0-9]{3}", item["date"]).group(0))
            except:
                date.text = "0000"

        description.text = item["description"]
        #date.text = item["date"]
        language.text = item["language"]
        relation.text = item["relation"]
        for i in item["identifier"]:
            identifier = ET.SubElement(element1, 'field')
            identifier.set('name', 'identifier')
            identifier.text = i
        ValidLink = ET.SubElement(element1, 'field')
        ValidLink.set('name', 'validLink')
        ValidLink.text=str(send_get_request(item["identifier"][0]))
        

        # Converting the xml data to byte object,
        # for allowing flushing data to file
        # stream
        b_xml = ET.tostring(data)
        b_xml = b_xml

        
        # Opening a file under the name `items2.xml`,
        # with operation mode `wb` (write + binary)
        with open("ReformattedData\\"+outputFile, "wb") as f:
            f.write(b_xml)
            count = count+1
            #print(count)
    return count


total = 0
import glob
txtfiles = []
for file in glob.glob("Metadata\\toFormat.xml"):
#for file in ["Metadata\\aaaaaaaa.xml"]:
    txtfiles.append(file)
    ls = file.split("\\")
    outputFile = ls[1]
    total = total + Extract(file, outputFile)
print("Total number of docs:", total)