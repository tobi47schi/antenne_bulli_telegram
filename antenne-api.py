import sys
import time
import requests

#ARGUMENTE

ersterSong = sys.argv[1]
zweiterSong = sys.argv[2]
bot_token = sys.argv[3]



def apiInfos():
    return requests.get('https://www.antenne.de/api/metadata/1.0/antenne/details?&apikey=c3e8228c8714e77f1544f95e7b9ebdee177bdcf8&livedata=&historyitemlimit=3').json()

def currentSong():
    r = apiInfos()
    now = r["data"]["now"]
    songNow = now["title"] + " - " + now["artist"]
    return songNow
    

def previousSong():
    r = apiInfos()
    previous = r["data"]["history"][0]
    previousSong = previous["title"] + " - " + previous["artist"]
    return previousSong


#REQUEST
def trefferSongs() :
    songNow = currentSong()
    songPrevious = previousSong()
    trefferZweiterSong = zweiterSong in songNow.lower()
    trefferErsterSong = ersterSong in songPrevious.lower()

    songReihenfolge = "1. " + songPrevious  + " ; 2. " + songNow

    return (trefferErsterSong and trefferZweiterSong)
    
def die_letzten_zwei_songs():
    r = requests.get('https://www.antenne.de/api/metadata/1.0/antenne/details?&apikey=c3e8228c8714e77f1544f95e7b9ebdee177bdcf8&livedata=&historyitemlimit=3').json()

    now = r["data"]["now"]
    previous = r["data"]["history"][0]

    songNow = now["title"] + " - " + now["artist"]
    previousSong = previous["title"] + " - " + previous["artist"]
    trefferZweiterSong = zweiterSong in songNow.lower();
    trefferErsterSong = ersterSong in previousSong.lower();

    songReihenfolge = "1. " + previousSong  + " \n 2. " + songNow
    return songReihenfolge

#TELEGRAM

telegram_api = 'https://api.telegram.org/bot'
my_bot_URL = telegram_api + bot_token

def telegram_bot_sendtext(bot_token, bot_chatID,bot_message):
    
    send_text = my_bot_URL + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message
    #https://api.telegram.org/bot[BOT_API_KEY]/sendMessage?chat_id=[CHANNEL_NAME]&text=[MESSAGE_TEXT]

    response = requests.get(send_text)
    return response.json()


def telegram_get_chat_ids():

    telegram_updates = requests.get(my_bot_URL + '/getupdates').json()
    chats = telegram_updates["result"]
    chat_id_list = []
    usernames = []
    for c in chats : 
        chat =  c["message"]["chat"]
        username= chat["username"]
        if username not in usernames:
            usernames.append(username)
            chat_id_list.append(str(chat["id"]))
    return chat_id_list
    


def telegram_send_to_channel (text) : 
    chat_ids = telegram_get_chat_ids()
    for chat_id in chat_ids:
        telegram_bot_sendtext(bot_token,chat_id,text)
        


while(True):
    try:
        localtime = time.localtime()
        now = time.strftime("%I:%M:%S %p", localtime)
        print(die_letzten_zwei_songs())
        if(trefferSongs()):
            telegram_send_to_channel(die_letzten_zwei_songs() + "\n 01375 / 100 100")
            sys.exit()
    except:
        print("Exception")
    time.sleep(5)


