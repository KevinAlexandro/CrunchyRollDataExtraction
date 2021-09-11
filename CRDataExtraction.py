import cloudscraper
import os
import xml.etree.ElementTree as ET
import json

def getAllCatalogue():
    #create scraper
    scraper = cloudscraper.create_scraper(browser={'platform': 'windows','mobile': False},interpreter = 'nodejs')
    #ajax string request -  dynamic from pg=1 to inf?
    ajaxRequest = "https://www.crunchyroll.com/videos/anime/popular/ajax_page?pg="
    #initialize
    pageNumber = 1
    pageText = "notEmpty"
    pageContent = "<li id="
    #always get a fresh xml file
    if os.path.exists("xmlData/catalogue.xml"):
        os.remove("xmlData/catalogue.xml")
    #extract data
    with open("xmlData/catalogue.xml",'a', encoding='utf-8') as f:
        f.write("<catalogue>")
        while "<li id=" in pageContent:
            pageHtml = scraper.get(ajaxRequest + str(pageNumber))
            pageText = pageHtml.text
            pageContent = str(pageHtml.content)
            pageNumber = pageNumber + 1
            #split each line of page text
            for line in pageText.splitlines():
                if "<a title=\"" in line:
                    f.write("\n"+line+"</a>")
        f.write("\n"+"</catalogue>")
    return

def getAllEpisodes():
    scraper = cloudscraper.create_scraper(browser={'platform': 'windows','mobile': False},interpreter = 'nodejs')
    headUrl = "https://www.crunchyroll.com"
    #extract info from xml
    tree = ET.parse('xmlData/catalogue.xml')
    root = tree.getroot()
    for child in root:
        videoRequest = headUrl + child.attrib["href"]
        pageHtml = scraper.get(videoRequest)
        pageText = pageHtml.text
        fileName:str = child.attrib["href"] + ".xml"
        fileName = fileName.replace("/","")
        fileName = "xmlData/" + fileName
        #always get a fresh xml file
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName,'a', encoding='utf-8') as f:
            f.write("<episodes>\n")
            for line in pageText.splitlines():
                if "$(\"#showview_videos_media" in line:
                    cleanLine = line.split(".data(\'bubble_data\', {")[1]
                    cleanLine = cleanLine.split(",\"description\":")[0]
                    cleanLine = cleanLine.replace("\"name\":","name = ")
                    #proper xml format
                    #Ampersand
                    cleanLine = cleanLine.replace("&","&amp;")
                    #double-quotation mark
                    cleanLine = cleanLine.replace("\\\"","&quot;")
                    #apostrophe
                    cleanLine = cleanLine.replace("'","&apos;")
                    #less than
                    cleanLine = cleanLine.replace("<","&lt;")
                    #greather than
                    cleanLine = cleanLine.replace(">","&gt;")
                    numberOfQuotes = cleanLine.count("\"")
                    if numberOfQuotes %2 != 0:
                        cleanLine = cleanLine+"\""
                    f.write("<episode "+ cleanLine + "></episode>\n")
            f.write("</episodes>")
    return

def generateJson():
    headUrl = "https://www.crunchyroll.com"
    #generate dict
    crunchyRollSeries = {}
    #extract info from xml
    catalogueTree = ET.parse('xmlData/catalogue.xml')
    catalogueRoot = catalogueTree.getroot()
    row =0
    for serie in catalogueRoot:
        serieName = serie.attrib["title"]
        serieUrl = headUrl + serie.attrib["href"]
        #for each serie
        #extract info from xml
        fileName:str = serie.attrib["href"] + ".xml"
        fileName = fileName.replace("/","")
        fileName = "xmlData/" + fileName
        parser = ET.XMLParser(encoding="utf-8")
        seriesTree = ET.parse(fileName, parser = parser)
        seriesRoot = seriesTree.getroot()
        episodeID = 0
        for episode in seriesRoot:
            episodeID = episodeID + 1
            row = row + 1
            episodeName = episode.attrib["name"]
            crunchyRollSeries[str(row)] = {"title" : serieName,"url" : serieUrl, "type":"Episode", "show_title" : episodeName}
        #single episode >> it is a show/movie
        if episodeID == 0:
            row = row + 1
            crunchyRollSeries[str(row)] = {"title" : serieName,"url" : serieUrl, "type":"Show", "show_title" : None}
    #print to dict to Json file
    with open('crunchyRollSeries.json', 'w') as f:
        json.dump(crunchyRollSeries, f)
    return


#get all popular shows
catalogueFlag = 0
while catalogueFlag == 0:
    try:
        getAllCatalogue()
        catalogueFlag = 1
    except:
        pass

#getAll Episodes of all shows
episodesFlag = 0
while episodesFlag == 0:
    try:
        getAllEpisodes()
        episodesFlag = 1
    except:
        pass

#generate local Json
generateJson()