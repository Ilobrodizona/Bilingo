import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import time

PAROLE_GIOCO = {
    "1": {
        "nome": "Facile 🟢",
        "dizionario": {"gatto": "cat", "cane": "dog", "mela": "apple", "casa": "house", "libro": "book"}
    },
    "2": {
        "nome": "Medio 🟡",
        "dizionario": {"finestra": "window", "tastiera": "keyboard", "scuola": "school", "giardino": "garden", "strada": "street"}
    },
    "3": {
        "nome": "Difficile 🔴",
        "dizionario": {"Aiuola": "flowerbed", "Soqquadro": "disarray", "Sfacciato": "cheeky", "Sconcertante": "baffling", "Appagante": "fulfilling"}
    }
}

def stampa_titolo():
    print("=" * 50)
    print(" ENGLISH VOICE BILINGO GAME ")
    print("=" * 50)
    print("Traduci la parola italiana pronunciandola in INGLESE!\n")

def avvia_gioco():
    stampa_titolo()
    
    print("Scegli il livello di difficoltà:")
    print("1. Facile (Parole comuni)")
    print("2. Medio (Parole quotidiane)")
    print("3. Difficile (Parole complesse)")
    
    scelta_diff = input("Inserisci il numero della difficoltà (1, 2 o 3): ").strip()
    if scelta_diff not in PAROLE_GIOCO:
        print("Scelta non valida, impostata modalità FACILE di default.")
        scelta_diff = "1"
        
    Livello = PAROLE_GIOCO[scelta_diff]
    dizionario_parole = list(Livello["dizionario"].items())
    
    punteggio = 0
    vite = 3
    durata = 4
    sample_rate = 44100
    recognizer = sr.Recognizer()

    print(f"\n🚀 Hai scelto la modalità: {Livello['nome']}")
    print("Hai 3 vite a disposizione. Buon divertimento!\n")
    time.sleep(1)

    while vite > 0 and len(dizionario_parole) > 0:
        parola_it, traduzione_en = random.choice(dizionario_parole)
        dizionario_parole.remove((parola_it, traduzione_en))

        print("-" * 40)
        print(f"❤️ Vite: {'❤️ ' * vite} | 🏆 Punteggio: {punteggio}")
        print(f"🇮🇹 Traduci in inglese la parola: ** {parola_it.upper()} **")
        
        input("Premi INVIO quando sei pronto a registrare...")
        
        print("🎙️ Parla ora in inglese...")
        recording = sd.rec(int(durata * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()
        wav.write("output.wav", sample_rate, recording)
        print("✅ Registrazione completata, riconoscimento in corso...")

        try:
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)
                
            testo_utente = recognizer.recognize_google(audio, language="en-US").strip().lower()
            print(f"📝 Hai detto: '{testo_utente}' (Corretto: '{traduzione_en}')")

            if traduzione_en in testo_utente:
                print("🎉 Ottimo! Risposta esatta! (+10 punti)")
                punteggio += 10
            else:
                print(f"❌ Sbagliato! La traduzione corretta era '{traduzione_en}'. (-1 vita)")
                vite -= 1

        except sr.UnknownValueError:
            print("Non ho udito alcuna voce o non ho capito. (-1 vita)")
            vite -= 1
        except sr.RequestError as e:
            print(f"⚠️ Errore di servizio di riconoscimento: {e}")

        time.sleep(1)

    print("\n" + "=" * 50)
    if vite == 0:
        print("💀 GAME OVER! Hai terminato le vite.")
    else:
        print("🏆 COMPLIMENTI! Hai completato tutte le parole della modalità!")
    print(f"🏁 Punteggio finale totalizzato: {punteggio} punti.")
    print("=" * 50)

if __name__ == "__main__":
    avvia_gioco()