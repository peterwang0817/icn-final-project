class Generic:
    """Generic class that implements basic debugging and printing. All objects that use print should inherit from this class.\n
    Methods:\n
    _print(string): prints a string to console, regardless of whether debug is toggled.
    _print_debug(string): prints a string to console, if debug is on.
    """
    def __init__(self, debug=False):
        self.name = 'RTSP Request Handler'
        self.debug = debug
        
    def _print(self, s):
        print('[{0}]: {1}'.format(self.name, s))
        
    def _print_debug(self, s):
        if self.debug: self._print(s)