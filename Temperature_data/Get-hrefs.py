import xml.etree.ElementTree as ET
import requests

href = "https://opendata-download-metobs.smhi.se/api/version/latest"
root = ET.fromstring(requests.get(href).text)

#for i in range(len(root)):
    #print("Title: ", root[i][0].text, "href:", root[i][2].text)

print(root.attrib)
for child in root:
    print(child.tag, child.attrib)