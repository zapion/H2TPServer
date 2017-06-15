def close_FFs():
    try:
        App.close("Nightly")
    except:
        pass
    try:
        App.close("Mozilla Firefox")
    except:
        pass

def launch_nightly():
    App.open("C:\\Program Files\\Nightly\\firefox.exe")
    makeSureNewTab()

def makeSureNewTab():
    while True:
        try:
            wait("1496306757186.png", 3)
            break
        except:
            print(' Wait for awesome bar, 1st failure, create a new tab.')
            click("1496312389216.png") 
    try:
        wait("1496306757186.png", 3)
    except:
        print(' Wait for awesome bar, 2nd failure.')

def passThroughAd():
    try:
        print("waiting to find skip add")
        if wait("1497345606141.png", 10):
            print("There's a Skip-the-Ad button ! click it")
            click("1497345606141.png") 
    except:
        print(" CAN NOT FIND !!")
        pass

close_FFs()
launch_nightly()
passThroughAd()

if not exists("1496306757186.png"):
    makeSureNewTab()
 
click("1496306757186.png")


type("https://www.youtube.com/watch?v=riZBFSEDTWQ")
type(Key.ENTER)
video_playback_region = Region(187,146,1069,521)
video_center = video_playback_region.getCenter()

while True:
    passThroughAd() 
    hover(video_center)
    if exists("1496395627376.png"):
        print("Good, it seems playing")
        rightClick(video_center)
        wait(0.5)
        click(Location(video_center.getX()+ 50, video_center.getY() + 270))
        break
    sleep(0.1)
while True:
    m = video_playback_region.wait("1496395288342.png", 800)
    if m is not None:
        print('Playback seems to the end !! Great !')
        close_FFs()
        break