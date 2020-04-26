# script for taking the submission_ssa.json, submission screenshots, and submission audio and
# combining them into a single mp4 file in clips
#
# written by Terence Lo
#
from moviepy.editor import *
import json
import helpfulFuncs as hf


resizeNeeded = False
#resizeNeeded = True
hf.empty_folder("artifacts/clips")

# vars
dim = (1280,720) #720p # video dimensions
w = 1200 #width of image should be <= to width of dim
h = 720 #height of image should be <= height of dim
bg_color = (26,26,27)  # reddit dark mode bg color, dark-dark-grey #1A1A1B
like_or_clip = VideoFileClip(f"misc/kanye-like-or.mp4")

# Read submission_ssa.json and save to variable selfss_and_a
selfss_and_a = []
with open('artifacts/jsons/submission_ssa.json', 'r') as filehandle:
    selfss_and_a = json.load(filehandle)
filehandle.close()


#resize screenshots
if resizeNeeded:
    hf.resizeSubmissionSS(w,h)


# Create a clip for concatenating the looped clips onto. This will be written to mp4 file for later
temp_clip = ColorClip(size=dim, color=bg_color, ismask=False, duration=(00.05))


# loop through lists in selfss_and_a and make a clip out of the screenshots and audio saved there
for l in selfss_and_a:
    try:
        f = open(l[0])
    except:
        print('Alert: File \'' + l[0] + '\' does not exist')  # do nothing
    else:  # do all this if it exists
        audio = AudioFileClip(l[1])
        audio = audio.volumex(1.8)

        imageC = (ImageClip(l[0])
                  .set_duration(audio.duration)
                  # .resize(width=w)
                  .on_color(size=dim,
                            color=bg_color)  # set screenshot on top of colorclip with bg_color as background color
                  .set_fps(5)
                  .set_position(("center", "center"))
                  .set_audio(audio))
        '''bg_pic.set_duration(audio.duration)  #set duration for big_pic imageclip
        imageC = CompositeVideoClip([bg_pic, imageC], size=dim).set_duration(audio.duration)  #set screenshot imageC on top of bg_pic imageclip'''

        temp_clip = concatenate_videoclips([temp_clip, imageC])
        print('Concatenated clip \'' + str(l[0]) + '\'' + ' to submission temp clip')
    finally:
        f.close()
# END for l in selfss_and_a loop


temp_clip = concatenate_videoclips([temp_clip, like_or_clip])

temp_clip.write_videofile('artifacts/clips/0intro.mp4')

temp_clip.close()
imageC.close()
audio.close()