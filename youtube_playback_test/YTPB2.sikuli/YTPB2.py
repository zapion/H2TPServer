import os
import logging
import sys
import errno
import shutil
from datetime import date


Settings.DebugLogs = False
Settings.InfoLogs = True
Debug.off()

# append system lib path
libs = ['C:\\Users\\user\\Projects', 'C:\\Miniconda2\\lib\\site-packages']
sys.path.extend(libs)
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


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

    def seek(driver, percent=50):
        from selenium.webdriver.common.action_chains import ActionChains
        if not driver or not isinstance(percent, int):
            print("input error, no driver instance or wrong percentage argument")
            return False
        progress_bar = driver.find_element_by_class_name("ytp-progress-bar")
        print("progress bar found")
        _seek = ActionChains(driver).move_to_element_with_offset(
                progress_bar,
                progress_bar.size['width'] * percent / 100,
                progress_bar.size['height'] / 2).click()
        print("seek action built")
        _seek.perform()
        print("seek action performed")

        return True
    
    binary = FirefoxBinary("C:\\Program Files\\Nightly\\firefox.exe")
    try:
        firefox = Firefox(firefox_binary=binary)
    except OSError:
        print(sys.exc_info())
    print("nightly launching...")
    sleep(5)
     
    # passThroughAd()


    v_link = "https://www.youtube.com/watch?v=riZBFSEDTWQ"
    isEng = True
    video_playback_region = Region(104,138,638,356)

    video_center =  video_playback_region.getCenter()
    firefox.get(v_link)
    
    start_playback_counter = 100 
    start_playback = False

    for _ in range(5):
        print("wait for pre-skip text to make sure page loaded")
        sleep(1)
        try:
            if firefox.find_element_by_class_name('videoAdUiPreSkipText'):
                sleep(5)
                break
        except NoSuchElementException as e:
            pass
    try:
        print("try to click skip ad")
        ad = firefox.find_element_by_class_name("videoAdUiSkipButton")
        if ad:
            print("ad found, click skip ad")
            ad.click()
    except NoSuchElementException as e:
        print("No skip ad, process to target video")
    except ElementNotInteractableException as e:
        print("Can't process click; element not interactable")

    print("right click for statistics")
    wait(0.5)
    rightClick(video_center)
    wait(0.5)
    offset_x = 50
    offset_y = 210 
    click(Location(video_center.getX()+ offset_x, video_center.getY() + offset_y))

    playback_done = False

    # pause for 5 secound here
    play = firefox.find_element_by_class_name("ytp-play-button")
    play.click()
    wait(5)
    play.click()
    wait(2)
    seek(firefox, 80)
    wait(2)
    
    print("start to fetch progress bar")
    progress_bar = firefox.find_element_by_class_name("ytp-progress-bar")
    video_max = int(progress_bar.get_attribute("aria-valuemax"))
    while True:
        running_sec = int(progress_bar.get_attribute("aria-valuenow"))
        if running_sec + 5 > video_max:
            print('Playback seems to the end !! Great !')
            break
        sleep(1)
        
    firefox.quit()
    playback_done = True
    result = 'YT link = {}, Playback Start = {}, Playback End = {}'.format(v_link, start_playback, playback_done)

    filename = os.path.join(final_folder, 'YT_Playback.txt')
    f = open(filename, 'w')
    f.write(result)
    f.close()


if __name__ == '__main__':
    main()