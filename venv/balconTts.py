'''
balconTts.py

generates TTS with UK Daniel_Full_22kHz voice - sounds memey
'''
import subprocess

balcon_location = f"C:/Users/Terence/PycharmProjects/reddit_tts_yt_bot/venv/balcon.exe"

def gen_tts(s, filename):
    process = subprocess.run(f"balcon -t \"{s}\" -w {filename}")
