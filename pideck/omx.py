from omxplayer.player import OMXPlayer


class Omx:
    def __init__(self):
        self.player = None
        
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
        
    def status(self):
        if not self.player:
            return {
                'status': 'stopped',
                'source': None,
            }
    
        return {
            'status': self.player.playback_status(),
            'source': self.player.get_source(),
            'position': self.player.position(),
            'duration': self.player.duration(),
            'volume': self.player.volume(),
        }