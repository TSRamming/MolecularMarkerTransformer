from lxml import etree
from datetime import datetime

root = etree.Element("OnkostarEditor")
tree = etree.ElementTree(root)
InfoXML = etree.SubElement(root, "InfoXML")
DatumXML = etree.SubElement(InfoXML, "DatumXML")
DatumXML.text = datetime.today().strftime('%Y-%m-%d')
Name = etree.SubElement(InfoXML, "Name")
Name.text = "Onkostar"
Version = etree.SubElement(InfoXML, "Version")
Version.text = "3.0.0-SNAPSHOT"





with open('test.xml', 'wb') as file:
    tree.write(file, encoding='utf-8')