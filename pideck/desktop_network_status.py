import subprocess
import time
from multiprocessing import Process
from .status_image_builder import StatusImageBuilder


def continuous_update_thread(interval):
    image_builder = StatusImageBuilder()
    
    while 1:
        try:
            image_builder.generate('/tmp/status.png')
            subprocess.run(['pcmanfm', '--set-wallpaper', '/tmp/status.png'])
        except Exception:
            print("Unable to update desktop with network status")
            
        time.sleep(interval)


def show_continuous_status(interval):
    p = Process(target=continuous_update_thread, args=(interval,))
    p.daemon = True
    p.start()