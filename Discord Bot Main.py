'''
Skippy Flatrock
Discord Bot for BTK Server

v 1.1
    add daily holiday
v 1.0.1
    Optimized Reload function
v 1.0
    added Text source file for user input and responce.
'''
import csv
import datetime
import os
import random

import discord
from dotenv import load_dotenv

import Resource.bible as bible
import Resource.youtubeLookup as YoutubeLookup

'''from bs4 import BeautifulSoup
#import urllib2
import urllib.request as r
soup = BeautifulSoup(r.urlopen("https://www.checkiday.com").read())
#print (r.urlopen("https://www.checkiday.com").read())
print(soup.get_text())#'''

load_dotenv(".env")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

def readFile (filepath):
    file = open(filepath, "r")
    lines = file.readlines()
    file.close()
    return lines

def isStringReplace (List,ReplaceEE,ReplaceR):
    #print ("List:",List)
    for i in range(len(List)):
        #print ("index:",i,"List part:",List[i])
        if isinstance(List[i],list):
            List[i] = isStringReplace(List[i],ReplaceEE,ReplaceR)
        elif isinstance(List[i],str):
            List[i] = List[i].replace(ReplaceEE,ReplaceR)
    return List

def defineResponses(client):
    #lines = readFile("Source/Responses.txt") # read source text
    responceCount = 0
    linesPrep = False
    count  = 0
    inputList = []
    settingsList = []
    outputList = []
    temp = []
    with open('Source/Responses.csv', mode ='r')as file:
   
    # reading the CSV file
        csvFile = csv.reader(file)
        skipline=True
    # displaying the contents of the CSV file
        for line in csvFile:
    #for line in lines: # loops through each line of text
            if skipline:
                skipline = False
            elif line [0] != "":
                #print ("line start")
                temp = line
                #print (temp)
                settingsList.append(int(temp[0]))
                temp.pop(0)
                #print (temp)
                inputList.append(temp[0])
                temp.pop(0)
                #print (temp)
                popbuffer = 0
                for out in range(len(temp)):
                    #print ("temp len:",len(temp),"out:",out,"popbuffer:",popbuffer,"total:",str(out+popbuffer))
                    if temp[out+popbuffer] == "":
                        #print ("poping:",temp[out+popbuffer])
                        temp.pop(out+popbuffer)
                        popbuffer=popbuffer-1
                #outtemp =[]
                outputList.append(temp)
        file.close()
            
    # ~ ~ ~ Clean up and print response array to terminal            
    outputList = isStringReplace(outputList,"\\n","\n")
    inputList = isStringReplace(inputList,"\\n","\n")
    print ("Input:",inputList) # may need a for loop to replace \\n to \n
    print("Output:",outputList)
    print("settingsList:",settingsList)
    print ("*** Responses Recived ***")
    inputList, outputList, settingsList, client= defineResponsesEvents(inputList, outputList, settingsList, client)
    return inputList, outputList, settingsList, client     
def channelBlackList(message, blackList):
    for item in blackList:
        if message.channel.id != item:
            return False
    return True 
def defineResponsesEvents(inputList, outputList, settingsList, client):# ~ ~ ~ Define client events
    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        #PRINT SERVER NAME
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        #show memebers of server
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    @client.event
    async def on_message(message):#ping quotes
        messageSendOk = True
        
        for item in [1005988104529772714,1005987759275638784]:
            if message.channel.id == item:
                messageSendOk = False
        print ("Message Recived:",message.content,"|Channel id:",message.channel.id,"|Ok to respond?",messageSendOk)
        #print(repr(message))
        if messageSendOk:
        #if message.channel.id != 1005987759275638784: #cm-chat id 
            
            #print ("progress: 1")
            if message.author == client.user:#checks to make sure it is not responding to it self.
                print ("Ignoring message sent by me!:",message.content)
                return
            
            #print ("progress: 2")
            if message.content.lower() == "reload responses":
                
                #reload()
                await message.channel.send("Reloading...")
                reload(client)
            
            #print ("testtt")
            contentt = message.content.lower()
            #print (contentt)
            #print (bible.searchVerse(contentt))
            if bible.searchVerse(contentt) == "404":
                print("No Bible Verse Found")
            else:
                await message.channel.send(bible.searchVerse(contentt))
                
                
            if message.content.lower() == "bot responses?":
                    await message.channel.send("You can use any of the following responses:"+ str(inputList))
            elif "holiday" in message.content.lower() and "today" in message.content.lower():
                dt = datetime.datetime.now()
                day = str(dt.strftime('%m/%d/%Y'))
                await message.channel.send(" https://www.checkiday.com/"+day+"") 
            elif "youtube search:" in message.content.lower():
                temp = message.content.lower().split("youtube search:")
                dt = datetime.datetime.now()
                day = str(dt.strftime('%m/%d/%Y'))
                links = YoutubeLookup.idsToURLs(YoutubeLookup.search(temp[1]))
                output ="You searched  \""+temp[1]+"\" on youtube:"
                for i in range(10):
                    output=output+"\n"+str(i+1)+": "+links [i]
                await message.channel.send(output)
            #elif message.content == 'raise-exception':
            #    raise discord.DiscordException 
            else: 
                for i in range (len(inputList)):
                    if settingsList[i] ==0:    
                        if isinstance(outputList[i],list):            
                            if inputList[i] in message.content.lower():
                                response = random.choice(outputList[i])
                                await message.channel.send(response)
                            elif message.content == 'raise-exception':
                                raise discord.DiscordException   
                        else:
                            if inputList[i] in message.content.lower():
                                await message.channel.send(outputList[i])
                            elif message.content == 'raise-exception':
                                raise discord.DiscordException
                    elif settingsList[i] ==1:
                        if isinstance(outputList[i],list):            
                            if message.content.lower() == inputList[i]:
                                response = random.choice(outputList[i])
                                await message.channel.send(response)
                            elif message.content == 'raise-exception':
                                raise discord.DiscordException   
                        else:
                            if message.content.lower() == inputList[i]:
                                await message.channel.send(outputList[i])
                            elif message.content == 'raise-exception':
                                raise discord.DiscordException
    print ("*** Resonses Primed ***")
    return inputList, outputList, settingsList, client     
def reload(client):
    print ("Reloading...")
    inputList, outputList, settingsList,client = defineResponses(client)
    return inputList, outputList, settingsList, client 
def closeMe(client):
    while not client.is_closed() or not client.is_ready():
        client.clear()
    print("~ ~ ~ Clearing Client ~ ~ ~")
print ("~ ~ ~ Client Started!! ~ ~ ~")
inputList = [""]
settingsList = [""]
outputList = [""]
client = discord.Client()
inputList, outputList, settingsList, client = defineResponses(client)
client.run(TOKEN)   
print ("~ ~ ~ Client closed!! ~ ~ ~")            
     