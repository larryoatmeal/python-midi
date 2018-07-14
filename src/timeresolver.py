from midi.tempomap import TempoMap


class TimeResolver(object):
    """
    iterates over a pattern and analyzes timing information
    the result of the analysis can be used to convert from absolute midi tick to wall clock time (in milliseconds).
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.tempomap = TempoMap(self.pattern)
        self.__resolve_timing()

    def __resolve_timing(self):
        """
        go over all events and initialize a tempo map
        """
        # backup original mode and turn to absolute
        original_ticks_relative = self.pattern.tick_relative
        self.pattern.make_ticks_abs()
        # create a tempo map
        self.__init_tempomap()
        # restore original mode
        if original_ticks_relative:
            self.pattern.make_ticks_rel()

    def __init_tempomap(self):
        """
        initialize the tempo map which tracks tempo changes through time 
        """
        for track in self.pattern:
            for event in track:
                if event.name == "Set Tempo":
                    self.tempomap.add(event)
        self.tempomap.update()

    def tick2ms(self, absolute_tick):
        """
        convert absolute midi tick to wall clock time (milliseconds)
        """
        ev = self.tempomap.get_tempo(absolute_tick)
        ms = ev.msdelay + ((absolute_tick - ev.tick) * ev.mpt)
        return ms
