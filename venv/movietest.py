#
# Script for testing random python stuff
#
#
from moviepy.editor import *
import json


#variables
dim = (1280,720) #720p # video dimensions
#dim = (854,480) #480p
#dim = (426,240) #240p
w = 1150 #width of image should be <= to width of dim
bg_color = (26,26,27)  # reddit dark mode bg color, dark-dark-grey #1A1A1B

a = ImageClip(f"misc/bg-pic.jpg")
audio = AudioFileClip(f"title/title_tts.mp3")
audio = audio.volumex(1.5)
image = (ImageClip(f"title/Capture.PNG")
	.resize(width=w)
	.set_fps(5)
	.set_audio(audio)
	.set_position(("center","center")))
image = CompositeVideoClip([a,image], size=dim).set_duration(audio.duration)

image.write_videofile('test-image.mp4')




'''
a = VideoFileClip(f'yt_movie.mp4')
b = AudioFileClip(f'misc/looped_music.wav')
b = b.set_duration(a.duration)
final_audio = CompositeAudioClip([a.audio, b])
final_clip = a.set_audio(final_audio)
final_clip.write_videofile('final_video2.mp4')



a = AudioFileClip(f'misc/looped_music_start.wav')
b = AudioFileClip(f'misc/looped_music.wav')
i = 0
while i<10:
	a = concatenate_audioclips([a, b])
	i+=1
a.write_audiofile('looped_music.wav')

# improvising an outro clip with moviepy
a = (ImageClip(f'title/outro.png')
    .set_duration(15.00)
	.resize(width=1280)
	.set_fps(5))
a.write_videofile("z_outro.mp4")


a = ColorClip(size = (1280,720), color =(26,26,27), ismask= False, duration=(00.05))
b = VideoFileClip(f"yt_movie.mp4")
final_clip = concatenate_videoclips([a,b])
final_clip.write_videofile("movietest.mp4")
final_clip.close()
a.close()
b.close()
'''

'''
my_list = ['geeks', 'for', 'geeks', 'like',
           'geeky', 'nerdy', 'geek', 'love',
           'questions', 'words', 'life']

# Read comments_list json and save to variable comments_list
comments_list = []
with open('title/comments_json.txt', 'r') as filehandle:
    comments_list = json.load(filehandle)
filehandle.close()

# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


# list should have
n = 5

x = list(divide_chunks(my_list, n))
print(x)
print(my_list)
'''