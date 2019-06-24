#!/usr/bin/env python3
import feedparser
import os

def openFiles():
    master = open('/home/pi/Documents/Show Cheker/Shows','r')
    new = open('/home/pi/Documents/Show Cheker/Shows.back','w')
    down = open('/home/pi/Desktop/Download','a')
    return master,new,down

def openRSS(url):
    #url="/home/pi/Desktop/71.rss"
    return feedparser.parse(url)

def formatEpisode(title):
    se=""
    #Find the position of the Episode Number
    pos=title.find("x")
    #Form the string
    for x in range(pos-2,pos+3):
        se=se + title[x]
        se=se.strip()
    return se


master,temp,down = openFiles()
newWrites = 0
#Main Loop
for line in master:
    #Get the actual line prepared TITLE;URL;LAST-EPISODE
    show = line.strip("\n").split(";")
    #Open the RSS
    feedRSS=openRSS(show[1])
    #Initialize the RSS counter
    i=len(feedRSS.entries)-1
    print ("Now processing: " + show[0] + "\n")
    while i>=0:
        #We dont want huge files or weirdly formated
        tooMuchQuality=feedRSS.entries[i].title.find("720")
        rightFormat=feedRSS.entries[i].title.find("x")
        if (tooMuchQuality == -1 and rightFormat > 0):
            episode=formatEpisode(feedRSS.entries[i].title)
        else:
            #Because episode needs to be initialized set it to 0x00
            #So it wont override the last episode seen
            episode="0x00"
        if (int(episode.replace("x","")) > int(show[2].replace("x",""))):
            #Write the episode link
            down.write(feedRSS.entries[i].link+"\n")
            newWrites = newWrites +1
            show[2]=episode
        i=i-1
    temp.write(";".join(show)+"\n")

print (newWrites,"new episodes.")
input()
down.close()
master.close()
temp.close()
if (newWrites == 0):
	os.remove("/home/pi/Desktop/Download")
os.remove("/home/pi/Documents/Show Cheker/Shows")
os.rename("/home/pi/Documents/Show Cheker/Shows.back","/home/pi/Documents/Show Cheker/Shows")
