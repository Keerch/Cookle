import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import pyautogui
import math
import re
import googletrans
import datetime
import wikipedia
import time
import wolframalpha
import translators as tlumacz
import requests
from pydub import AudioSegment
from pydub.playback import play
import io
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

# Inicjalizacja urządzeń dźwiękowych
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Inicjalizacja tłumacza
translator = googletrans.Translator()

# Inicjalizacja rozpoznawania mowy
r = sr.Recognizer()

# Inicjalizacja syntezatora mowy
engine = pyttsx3.init()

# Funkcja do wysyłania tekstu do API i otrzymywania URL z nagraniem głosowym
def speak(text, speaker_id):
    api_url = 'https://api.topmediai.com/v1/text2speech'
    headers = {
        'accept': 'application/json',
        'x-api-key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'Content-Type': 'application/json'
    }
    body = {
        'text': text,
        'speaker': speaker_id,
        'emotion': 'Neutral'
    }

    response = requests.post(api_url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json().get('data')
        audio_url = data.get('oss_url')
        if audio_url:
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                audio_stream = io.BytesIO(audio_response.content)
                audio = AudioSegment.from_file(audio_stream)
                play(audio)
            else:
                print("Nie udało się pobrać pliku audio.")
        else:
            print("URL pliku audio nie jest dostępny.")
    else:
        print("Wystąpił błąd:", response.status_code)

# Funkcja, która wysłuchuje polecenia od użytkownika
def listen():
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        print("Udało sie rozpoznac mowe")
        return r.recognize_google(audio, language="pl-PL")
    except sr.UnknownValueError:
        speak("danno what you mean", "001565ad-3826-11ee-a861-00163e2ac61b")
        return ""
    except sr.RequestError as e:
        print("Błąd podczas łączenia z serwerem rozpoznawania mowy: {0}".format(e))
        return ""
def shutdown_computer():
  subprocess.call(["shutdown", "-s", "-t", "60"])
  speak("Killing your PC in 60 second.", "001565ad-3826-11ee-a861-00163e2ac61b")


def open_website(website):
  # Otwórz podany adres URL w domyślnej przeglądarce
  webbrowser.open(website)

# Słownik zawierający nazwy stron internetowych i odpowiadające im adresy URL
websites = {
  "Google": "https://www.google.com",
  "YouTube": "https://www.youtube.com",
  "Wikipedia": "https://www.wikipedia.org"
}
def zoom_in():
  # Przybliż obraz za pomocą skrótu klawiszowego Ctrl + +
  pyautogui.hotkey("ctrl", "+")

def zoom_out():
  # Przybliż obraz za pomocą skrótu klawiszowego Ctrl + -
  pyautogui.hotkey("ctrl", "-")

def open_application(application):
  # Otwórz podaną aplikację za pomocą polecenia systemowego start
  subprocess.call(["start", application], shell=True)

# Słownik zawierający nazwy aplikacji i odpowiadające im ścieżki do plików wykonywalnych
applications = {
  "kalendarz": "C:\\Program Files\\Windows Calendar\\Calendar.exe",
  "notatnik": "C:\\Windows\\notepad.exe",
  "Paint": "C:\\Windows\\System32\\mspaint.exe"
}
#Słownik zawierający nazwy języków i odpowiadające im kody języków używane przez bibliotekę googletrans
languages = {
  "angielski": "en",
  "niemiecki": "de",
  "francuski": "fr",
  "hiszpański": "es"
}

def set_volume(level):
  # Zmień głośność systemu na podany poziom (od 0 do 100)
  volume.SetMasterVolumeLevelScalar(level*0.01,None)

def mute_sound(m):
   # Włącz/wyłącz wyciszenie głośności systemu
   volume.SetMute(m, None)
def przywitanie():
    godzina = datetime.datetime.now().hour
    if godzina >= 0 and godzina < 19:
      speak("Eyy what's up?", "001565ad-3826-11ee-a861-00163e2ac61b")
    elif godzina >= 18 and godzina < 24:
      speak("Eyy Hi", "001565ad-3826-11ee-a861-00163e2ac61b")

def pozegnanie():
  godzina = datetime.datetime.now().hour
  if godzina > 0 and godzina <= 18:
    speak("goodbye", "001565ad-3826-11ee-a861-00163e2ac61b")
  elif godzina > 18 and godzina <= 24:
    speak("goodbye", "001565ad-3826-11ee-a861-00163e2ac61b")

def calculate(expression):
    # Użyj wyrażenia regularnego, aby usunąć z polecenia od użytkownika słowa takie jak "oblicz" i "wynik"
    expression = re.sub(r"oblicz|wynik", "", expression)

    # Wykonaj obliczenia za pomocą funkcji eval i zwróć wynik
    return eval(expression)

def translate(text, dest_language):
    # Użyj biblioteki googletrans do tłumaczenia podanego tekstu na podany język
    translation = translator.translate(text, dest=dest_language)
    # Zwróć tłumaczenie
    return translation.text

  #Poproś użytkownika o wypowiedzenie polecenia
przywitanie()

  # Wysłuchaj polecenia od użytkownika
# Pętla główna aplikacji
while True:
  speak("Speak now", "001565ad-3826-11ee-a861-00163e2ac61b")
  command = listen()
  #Jeśli użytkownik powiedział "zakończ", zakończ działanie aplikacji
  #W pętli głównej aplikacji, sprawdź, czy polecenie od użytkownika to "wyłącz komputer"

  if "wyłącz" in command:
      speak("Shut down your computer", "001565ad-3826-11ee-a861-00163e2ac61b")
      #shutdown_computer()
  # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika to "otwórz stronę" i jaka strona ma być otwarta

  elif "Otwórz" in command:
    # Pobierz nazwę strony internetowej z polecenia
    website = command.split()[-1]
    # Sprawdź, czy nazwa strony znajduje się w słowniku websites
    if website in websites:
        # Otwórz stronę w przeglądarce
        open_website(websites[website])
    else:
            speak("Don't know this page ", "001565ad-3826-11ee-a861-00163e2ac61b")
  # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika to "przybliż obraz"
  elif "Przybliż obraz" in command:
      speak("zoom in", "001565ad-3826-11ee-a861-00163e2ac61b")
      zoom_in()

  elif "oddal obraz" in command:
      speak("zoom out", "001565ad-3826-11ee-a861-00163e2ac61b")
      zoom_out()

  # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika to "otwórz aplikację" i jaka aplikacja ma być otwarta
  elif "Uruchom aplikację" in command:
    # Pobierz nazwę aplikacji z polecenia
    application = command.split()[-1]
    # Sprawdź, czy nazwa aplikacji znajduje się w słowniku applications
    if application in applications:
      # Otwórz aplikację
      open_application(applications[application])
    else:
      speak("Don't know this app", "001565ad-3826-11ee-a861-00163e2ac61b")


  elif "Zakończ" in command:
    pozegnanie()
    break
  # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika zaczyna się od słowa "oblicz"
  elif command.startswith("Oblicz"):
      if "plus" in command:
        command = command.replace("plus", "+")
      elif "minus" in command:
        command = command.replace("minus", "-")
      elif "razy" in command:
        command = command.replace("razy", "*")
      elif "x" in command:
        command = command.replace("x", "*")
      elif "dzielone" and "na" in command:
        command = command.replace("dzielone", "/")
        command = command.replace("na", "")
      elif "do" and "potęgi" in command:
        command = command.replace("do", "**")
        command = command.replace("potęgi", "")
      # Pobierz wyrażenie matematyczne z polecenia
      try:
        expression = command.split("oblicz", 1)[1]
      except:
        expression = command.split("Oblicz", 1)[1]
      # Wykonaj obliczenia i zapisz wynik do zmiennej result
      result = calculate(expression)
      # Powiedz użytkownikowi wynik obliczeń
      speak("It's about... ", "001565ad-3826-11ee-a861-00163e2ac61b" + str(result))
      print("Wynik obliczeń to: " + str(result))


    # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika to "przetłumacz na"
    # i jaki język ma być użyty do tłumaczenia
  elif "tłumacz na" in command:
      # Pobierz język, na który ma być przetłumaczony tekst, z polecenia
      dest_language = command.split()[2]
      # Sprawdź, czy podany język znajduje się w słowniku languages
      if dest_language in languages:
        # Pobierz tekst, który ma być przetłumaczony, z polecenia

        text = command.split(dest_language, 1)[1]
        # Przetłumacz tekst i zapisz wynik do zmiennej result
        result = translate(text, languages[dest_language])
        # Powiedz użytkownikowi wynik tłumaczenia
        speak("This is: ", "001565ad-3826-11ee-a861-00163e2ac61b" + result)
      else:
        speak("Don't know what you're talking about", "001565ad-3826-11ee-a861-00163e2ac61b")

    # W pętli głównej aplikacji sprawdź, czy polecenie od użytkownika to "ustaw głośność na"
    # i jaki poziom ma zostać ustawiony
  elif "głośność na" in command:
      # Pobierz poziom głośności z polecenia
      level = int(command.split()[-1])
      # Sprawdź, czy poziom głośności jest prawidłowy (od 0 do 100)
      if level >= 0 and level <= 100:
        # Ustaw głośność na podany poziom
        speak("Done"  , "001565ad-3826-11ee-a861-00163e2ac61b")
        set_volume(level)
      else:
        speak("Volume must be a value from 0 to 100", "001565ad-3826-11ee-a861-00163e2ac61b")

    # Wyłącz dźwięk systemowy
  elif "Wyłącz dźwięk" in command:
       mute_sound(1)

    # Włącz dźwięk systemowy
  elif "Włącz dźwięk" in command:
       mute_sound(0)

  else:
    speak("Repeat please " , "001565ad-3826-11ee-a861-00163e2ac61b"+ command)

