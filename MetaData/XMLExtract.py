import xml.etree.ElementTree as ET

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
            'identifier': identifier
        })

    return items



xml_file = 'MetaData/toFormat.xml'
items = parse_xml(xml_file)
#for item in items:
    #print(item)
#    pass


# This is the parent (root) tag
# onto which other tags would be
# created
data = ET.Element('add')

for item in items:
     
    # Adding a subtag named `Opening`
    # inside our root tag
    element1 = ET.SubElement(data, 'doc')

    # Adding subtags under the `Opening`
    # subtag
    title = ET.SubElement(element1, 'field')
    creator = ET.SubElement(element1, 'field')
    #subject = ET.SubElement(element1, 'field')
    description = ET.SubElement(element1, 'field')
    date = ET.SubElement(element1, 'field')
    identifier = ET.SubElement(element1, 'field')

    # Adding attributes to the tags under
    # `items`
    title.set('name', 'title')
    creator.set('name', 'creator')
    #subject.set('name', 'subject')
    description.set('name', 'description')
    date.set('name', 'date')
    identifier.set('name', 'identifier')

    # Adding text between the `E4` and `D5`
    # subtag
    title.text = "hello"
    creator.text = item["creator"]
    for i in item["subject"]:
        subject = ET.SubElement(element1, 'field')
        subject.set('name', 'subject')
        subject.text = i
    description.text = item["description"]
    date.text = item["date"]
    for i in item["identifier"]:
        identifier = ET.SubElement(element1, 'field')
        identifier.set('name', 'identifier')
        identifier.text = i


    # Converting the xml data to byte object,
    # for allowing flushing data to file
    # stream
    b_xml = ET.tostring(data)
    b_xml = b_xml

    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    with open("GFG.xml", "wb") as f:
        f.write(b_xml)