import urllib.request
import re

def search(search_parm):
    #search_keyword="mozart"
    search_parm=search_parm.replace(" ","+")#converts search term into url format
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_parm)#finds search page.
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())#consolidates search html to video ids
    unique_video_ids = []
    for id in video_ids:#picks out unique video ids
        if id not in unique_video_ids:
            unique_video_ids.append(id)
    return unique_video_ids #returns video ids
def idToURL(id):
    return"https://www.youtube.com/watch?v=" + id
def idsToURLs (ids):#returns video links from id input
    links =[]
    for id in ids:
            links.append(idToURL(id))
    return links


ids = search("skippy flatrock")
print(ids)
print(idsToURLs(ids))