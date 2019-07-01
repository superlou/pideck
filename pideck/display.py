import os


def set_display_mode(mode):
    if mode == 'blank':
        os.system('tvservice -o; tvservice -p')
    elif mode == 'off':
        os.system('tvservice -o')
    elif mode == 'desktop':
        os.system('tvservice -p; sleep 0.5s; fbset -depth 16; fbset -depth 32; xrefresh')
