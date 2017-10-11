import time
import threading
import pyperclip


from PIL import ImageGrab


import time
datestr = time.strftime("%Y%m%d")

def is_url_but_not_bitly(url):
    #if url.startswith("http://") and not "bit.ly" in url:
    return True
    #return False

def print_to_stdout(clipboard_content):

    print ("Found url: %s" % str(clipboard_content))

    
def savetofile(clipboard_content):
    print ('data found')
    datestr = time.strftime("%Y%m%d")
    f = open('clip-%s.txt'%datestr, 'a')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    f.write(timestr)
    f.write('\n')
    f.write('----------------------------------------------------------------------------\n')
    f.write(clipboard_content)
    f.write('\n')
    f.close()
    
    
class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):       
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            try:
                im = ImageGrab.grabclipboard()
                timestr = time.strftime("%Y%m%d-%H%M%S")
                im.save('c://dev/screenshots//screengrab_%s_%s.png'%(datestr,timestr), 'PNG')
                pyperclip.copy('')
                
            except:
                pass
            time.sleep(self._pause)
            

    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher(is_url_but_not_bitly, 
                               savetofile,
                               5.)
    watcher.start()
    while True:
        try:
            print ("Waiting for changed clipboard...")
            time.sleep(10)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    main()
    
