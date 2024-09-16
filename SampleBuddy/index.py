import __import
from Wdgt import *
#import ffmpeg
#from __ffmpeg import ffplay
#from ffmpeg import avcodec_decode_audio3
def ffplay(playAudio):
    print("+call ffmpeg")
if subprocess.call("ffmpeg -i ~/myMedia/mp4/vga50fps_1080p.mp4 ~/test.mkv", shell=True):
   raise Exception("{} failed!!!".format("ffmpeg"))
print("-call ffmpeg")
#// use ffmpeg here to perform various operations here

# Play Audio clip

def trackplay():
#while(stream_is_over):
# Copy the decoded raw buffer from native code to "buffer" .....
#............
    trackplay= trackplay(buffer, 0, readBytes, 0)
