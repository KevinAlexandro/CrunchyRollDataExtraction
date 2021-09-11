import json
import xml.etree.ElementTree as ET

headUrl = "https://www.crunchyroll.com"
#generate dict
crunchyRollSeries = {}
#extract info from xml
catalogueTree = ET.parse('xmlData/catalogue.xml')
catalogueRoot = catalogueTree.getroot()
row =0
tmpDict = {}
for serie in catalogueRoot:
    serieName = serie.attrib["title"]
    serieUrl = headUrl + serie.attrib["href"]
    #for each serie
    #extract info from xml
    fileName:str = serie.attrib["href"] + ".xml"
    fileName = fileName.replace("/","")
    fileName = "xmlData/" + fileName
    print(fileName)
    parser = ET.XMLParser(encoding="utf-8")
    seriesTree = ET.parse(fileName, parser = parser)
    seriesRoot = seriesTree.getroot()
    episodeID = 0
    for episode in seriesRoot:
        episodeID = episodeID + 1
        row = row + 1
        episodeName = episode.attrib["name"]
        tmpDict.clear()
        tmpDict["title"] = serieName
        tmpDict["url"] = serieUrl
        tmpDict["type"] = "Episode"
        tmpDict["show_title"] = episodeName
        crunchyRollSeries[row] = tmpDict

    #single episode >> it is a show/movie
    if episodeID == 0:
        tmpDict.clear()
        tmpDict["title"] = serieName
        tmpDict["url"] = serieUrl
        tmpDict["type"] = "Show"
        tmpDict["show_title"] = None
        row = row + 1
        crunchyRollSeries[row] = tmpDict

    #myJson = json.dump(crunchyRollSeries, indent=4)
    with open('crunchyRollSeries.json', 'w') as f:
        json.dump(crunchyRollSeries, f)