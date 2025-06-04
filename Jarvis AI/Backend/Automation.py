from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = [
    "ZCbbwF", "hgKElC", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzWSb YwPhnf", 
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "OSUR6d LTKOO", 
    "VLzY6d", "webanswers-webanswers_table__webanswers-table", 
    "dD0No ikb4Bb gsrt", "sXLAoE", "LWfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

client = Groq(api_key=GroqAPIKey)

messages = []

SystemChatBot = [{"role": "system", "content": "You're a content writer. You have to write content like letters."}]


def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    
    def OpenNotepad(File):
        subprocess.Popen(["notepad.exe", File])

    def ContentWriteAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
    model="llama3-70b-8192",  # or "mistral-7b-8192", "mixtral-8x7b-32768"
    messages=SystemChatBot + messages,
    max_tokens=2048,
    temperature=0.7,
    top_p=1,
    stream=True
)


        
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic = Topic.replace("Content", "").strip()
    ContentByAI = ContentWriteAI(Topic)
    filename = rf"Data\{Topic.lower().replace(' ', '_')}.txt"
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    
    OpenNotepad(filename)
    return True
Content("Wrie a leave letter")
def YoutubeSearch(Topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={Topic}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": user_agent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None
        
        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True

def CloseApp(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release('volume mute'),
        "unmute": lambda: keyboard.press_and_release('volume unmute'),
        "volume up": lambda: keyboard.press_and_release('volume up'),
        "volume down": lambda: keyboard.press_and_release('volume down')
    }
    if command in actions:
        actions[command]()
    return True

async def TranslateAndExecute(commands):
    funcs = []
    for command in commands:
        if command.startswith("open"):
            funcs.append(asyncio.to_thread(OpenApp, command[5:]))
        elif command.startswith("close"):
            funcs.append(asyncio.to_thread(CloseApp, command[6:]))
        elif command.startswith("play"):
            funcs.append(asyncio.to_thread(PlayYoutube, command[5:]))
        elif command.startswith("content"):
            funcs.append(asyncio.to_thread(Content, command[8:]))
        elif command.startswith("google search"):
            funcs.append(asyncio.to_thread(GoogleSearch, command[14:]))
        elif command.startswith("youtube search"):
            funcs.append(asyncio.to_thread(YoutubeSearch, command[15:]))
        elif command.startswith("system"):
            funcs.append(asyncio.to_thread(System, command[7:]))
        else:
            print(f"No function found for: {command}")
    
    results = await asyncio.gather(*funcs)
    return results

async def Automation(commands):
    results = await TranslateAndExecute(commands)
    print(f"Execution results: {results}")
    return True
