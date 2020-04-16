# script for taking the saved json, screenshots, and audio and combining them into a single mp4 file
#
# written by Terence Lo
#
from moviepy.editor import *
import json
import helpfulFuncs as hf
from PIL import Image


#variables
dim = (1280,720) #720p # video dimensions
w = 1200 #width of image should be <= to width of dim
h = 720 #height of image should be <= height of dim
bg_color = (26,26,27)  # reddit dark mode bg color, dark-dark-grey #1A1A1B
clip_filenames = []


# make a video clip for the static video effect
static_vf = VideoFileClip(f"misc/static_vf.mp4")
static_vf = static_vf.volumex(2.8)   #TODO fix static_vf/mp4 sound
# make an image clip for the background picture
#bg_pic = ImageClip(f"misc/bg-pic.jpg")


#clear clips folder
hf.empty_folder(f'artifacts/clips')


# Read comments_list json and save to variable comments_list
comments_list = []
with open('artifacts/title/screenshots_and_audios.json', 'r') as filehandle:
    comments_list = json.load(filehandle)
filehandle.close()
# groups_list: Divide comments list into a list of comment groups of 10 to resolve moviePy recursion error bug
groups_list = list(hf.divide_chunks(comments_list, 10))


#make "final" image clip using title screenshot and title audio tts. Every clip after this will be concatenated to final_clip
audio = AudioFileClip(f"artifacts/title/title_tts.mp3")
audio = audio.volumex(1.8)
imageC = (ImageClip(f"artifacts/title/Capture.PNG")
	.set_duration(audio.duration)
	.resize(width=w)
	.on_color(size=dim, color=bg_color)
	.set_fps(5)
	.set_position(("center","center"))
	.set_audio(audio))
'''bg_pic.set_duration(audio.duration)  #set duration of bg_pic
imageC = CompositeVideoClip([bg_pic,imageC], size=dim).set_duration(audio.duration)  #compose imageC on top of bg_pic'''
imageC.write_videofile('artifacts/clips/0intro.mp4')


group_i = 1 # 'group of 10' counter
#comment_i = 0 #comment counter

#loop through groups of 10, write a clip after putting all the pieces together
for group in groups_list:

	# Create a clip for concatenating the looped clips onto. This will be written to mp4 file for later
	temp_clip = ColorClip(size=dim, color=bg_color, ismask=False, duration=(00.05))

	#loop through comments in group
	for comment in group:

		# check if the screenshot exists and add static effect
		try:
			f = open(comment[0][0])
		except:
			print('Alert: File \'' + comment[0][0] + '\' does not exist, staticvf could not be added')  # do nothing
		else:  # do all this if it exists
			temp_clip = concatenate_videoclips([temp_clip, static_vf])
			print('Static vf added')
			#f.close()  #bug fix? if f cant be opened then it cant be closed in finally?
		finally:
			f.close()

		#sentence_i = 0 #sentence iterator

		for sentence in comment:

			#check if the screenshot exists, in case I deleted it between scripts which I will prob do a lot
			#if it doesnt exist do nothing and go to the next loop
			try:
				f = open(sentence[0])
			except:
				print('Alert: File \'' + sentence[0] + '\' does not exist')  # do nothing
			else:  #do all this if it exists
				audio = AudioFileClip(sentence[1])
				audio = audio.volumex(1.8)

				imageC = (ImageClip(sentence[0])
						 .set_duration(audio.duration)
						 #.resize(width=w)
						 .on_color(size=dim, color=bg_color)  #set screenshot on top of colorclip with bg_color as background color
						 .set_fps(5)
						 .set_position(("center", "center"))
						 .set_audio(audio))
				'''bg_pic.set_duration(audio.duration)  #set duration for big_pic imageclip
				imageC = CompositeVideoClip([bg_pic, imageC], size=dim).set_duration(audio.duration)  #set screenshot imageC on top of bg_pic imageclip'''

				temp_clip = concatenate_videoclips([temp_clip, imageC])
				print('Concatenated clip \'' + str(sentence[0]) + '\'' + ' to group ' + str(group_i) + ' clip')

				'''#  ------     Just in case I need to save the individual clips     --------
				imageC.write_videofile("artifacts/clips/clip_"+str(comment_i) +'_'+str(sentence_i)+'.mp4')
				print('saved clip ' + str(comment_i)+'_'+str(sentence_i))
				sentence_i += 1'''
			finally:
				f.close()
			# END sentences loop

		# END comments loop

	temp_clip.write_videofile("artifacts/clips/" + str(group_i) + "clip.mp4")
	clip_filenames.append("artifacts/clips/" + str(group_i) + "clip.mp4")
	group_i += 1
	# END groups_list loop


# Combine the clips into one final clip
final_clip = VideoFileClip(f"artifacts/clips/0intro.mp4")
for clip_filename in clip_filenames:
	temp_clip = VideoFileClip(clip_filename)
	final_clip = concatenate_videoclips([final_clip,temp_clip])


# add the outro to the final clip   #TODO make a better outro
temp_clip = VideoFileClip(f"misc/outro.mp4")
final_clip = concatenate_videoclips([final_clip, static_vf, temp_clip])
print('Static vf and outro added')


# Add looped music
#bg_music = AudioFileClip(f'misc/BetterDays-looped.wav')
bg_music = AudioFileClip(f'misc/Fun-openMU5IC-looped.wav')
bg_music = bg_music.set_duration(final_clip.duration)
bg_music = bg_music.volumex(0.2)  # Lower the volume of bg music
bg_music = CompositeAudioClip([final_clip.audio, bg_music])
final_clip = final_clip.set_audio(bg_music)


# Write the result to a file: "movie/yt_movie.mp4"
final_clip.write_videofile(f"artifacts/movie/yt_movie.mp4")


#close all clips to free up resources
final_clip.close()
temp_clip.close()
static_vf.close()
audio.close()
imageC.close()
#bg_pic.close()
bg_music.close()