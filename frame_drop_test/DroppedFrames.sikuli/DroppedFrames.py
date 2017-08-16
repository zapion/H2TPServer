import logging
import sys
import os
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
    filename=os.path.join(final_folder, "drop_frame.log"),
    filemode='a')

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl


def main():
    video_playback_region = Region(308,149,861,487)

    video_center =  video_playback_region.getCenter()

    def makeSureNewTab():
        count = 5
        while count > 0:
            try:
                wait("1497861542731.png", 0)
                break
            except:
                print(' Wait for awesome bar, 1st failure, create a new tab.')
                click("1502333115549.png")
            count -= 1
        try:
            wait("1497861542731.png", 5)
        except:
            print(' Wait for awesome bar, 2nd failure.')

    try:
        App.close("Nightly")
    except:
        pass

    App.open("C:\\Program Files\\Nightly\\firefox.exe")
    makeSureNewTab()

    if not exists("1496306757186.png"):
        makeSureNewTab()
 
    click("1497861631105.png")

    type("https://kilikkuo.github.io/H2TPServer/frame_drop_test")
    type(Key.ENTER)
    wait("1497858591311.png", 3)
    click("1497858591311.png")
    wait(300)
    s = Screen()
    result_region = Region(0,0,537,880)
    saved_img = s.capture(result_region)

    shutil.copy(saved_img.getFilename(), os.path.join(final_folder, 'dropped_frame_test_result.png'))
    App.close("Nightly")


if __name__ == '__main__':
    main()