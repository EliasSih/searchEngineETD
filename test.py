import xml.etree.ElementTree as ET
def getURL(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(root)
    for data in root.findall(".//doc"):
        if "field name='creator'" in data[0].text:
            print(data[1].text)
    for child in root:
        for subchild in child:
            print(subchild.attrib.text)
        #if data.find("field name=creator") is not None:
            pass
        #    print(data.find("field name=creator").text)
    for decade in root.findall(".//doc"):
        print(decade.attrib)
        for year in decade.findall("./doc/date"):
            print(year.text, '\n')
getURL("ReformattedData\\aaaaaaaa.xml")