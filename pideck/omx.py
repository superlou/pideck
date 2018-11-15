from omxplayer.player import OMXPlayer


class Omx:
    def __init__(self, media_folder):
        self.player = None
        self.media_folder = media_folder
        
    def play(self, filename):
        if self.player:
            self.player.load(filename)
        else:
            self.player = OMXPlayer(filename, args=['-b', '--no-osd'])
            
    def stop(self):
        if not self.player:
            return
        
        self.player.stop()
        self.player = None
            
    def pause(self):
        if not self.player:
            return
        
        self.player.play_pause()
        
    def seek_fraction(self, fraction):
        if not self.player:
            return
        
        duration = self.player.duration()
        self.player.set_position(fraction * duration)
        
    def get_source(self):
        """ Get player source and remove media folder """
        source = self.player.get_source()
        if source.startswith(self.media_folder + "/"):
            return source[len(self.media_folder) + 1:]
        else:
            return source
        
    def status(self):
        if not self.player:
            return {
                'status': 'stopped',
                'source': None,
            }
    
        return {
            'status': self.player.playback_status(),
            'source': self.get_source(),
            'position': self.player.position(),
            'duration': self.player.duration(),
            'volume': self.player.volume(),
        }