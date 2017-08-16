import os
import logging
import sys
import errno
import shutil
from datetime import date


class StreamToLogger(object):
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())


def makeSureResultFolderExist(result_date):
    desktop_path = os.path.join(os.environ["HOMEPATH"], 'Desktop')
    today = date.today()
    result_folder = os.path.join(desktop_path, 'sikuli_result', result_date.isoformat())
    if not os.path.exists(result_folder):
        try:
            os.makedirs(result_folder)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
    return result_folder

today = date.today()
final_folder = makeSureResultFolderExist(today)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename=os.path.join(final_folder, "youtube_test.log"),
    filemode='a')

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl




def close_FFs():
    try:
        App.close("Nightly")
    except:
        pass

def launch_nightly():
    App.open("C:\\Program Files\\Nightly\\firefox.exe")
    makeSureNewTab()

def makeSureNewTab():
    count = 5
    while count > 0:
        try:
            wait("1497861542731.png", 5)
            break
        except:
            print(' Wait for awesome bar, 1st failure, create a new tab.')
            click("1496312389216.png")
        count -= 1
    try:
        wait("1497861542731.png", 5)
    except:
        print(' Wait for awesome bar, 2nd failure.')

def passThroughAd():
    global isEng
    try:
        print("waiting to find skip ad (cht)")
        if video_playback_region.wait("1497345606141.png", 8):
            print("There's a skip-Ad button (cht) ! click it")
            isEng = False
            click("1497345606141.png") 
    except:
        print(" CAN NOT FIND !!")
        pass
    try:
        print("waiting to find skip ad (eng)")
        if video_playback_region.wait("1497861434126.png", 8):
            print("There's a skip-Ad button (eng) ! click it")
            isEng = True
            click("1497861434126.png") 
    except:
        print(" CAN NOT FIND !!")
        pass


def main():
    try:
        App.close("Nightly")
    except:
        pass

    App.open("C:\\Program Files\\Nightly\\firefox.exe")
    makeSureNewTab()

    passThroughAd()


    v_link = "https://www.youtube.com/watch?v=riZBFSEDTWQ"
    isEng = True
    video_playback_region = Region(308,149,861,487)

    video_center =  video_playback_region.getCenter()
    if not exists("1496306757186.png"):
        makeSureNewTab()
 
    click("1497861631105.png")

    type(v_link)
    type(Key.ENTER)

    start_playback_counter = 100 
    start_playback = False
    while start_playback_counter > 0:
        passThroughAd() 
        hover(video_center)
        if exists("1497923531328.png"):
            print("Good, it seems playing")
            rightClick(video_center)
            wait(0.5)
            offset_x = 50
            offset_y = 210 if isEng else 270
            print(' offset : {}'.format(offset_y))
            click(Location(video_center.getX()+ offset_x, video_center.getY() + offset_y))
            start_playback = True
            break
        sleep(0.1)
        start_playback_counter -= 1

    playback_done = False
    sleep(600)
    click("1502414988106.png")
    while True:
        
        m = video_playback_region.wait("1502415019705.png", 800)
        if m is not None:
            print('Playback seems to the end !! Great !')
            close_FFs()
            playback_done = True
            break

    result = 'YT link = {}, Playback Start = {}, Playback End = {}'.format(v_link, start_playback, playback_done)

    filename = os.path.join(final_folder, 'YT_Playback.txt')
    f = open(filename, 'w')
    f.write(result)
    f.close()


if __name__ == '__main__':
    main()