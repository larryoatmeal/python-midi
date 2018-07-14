import midi
import midi.timeresolver as tres
pattern = midi.read_midifile("mary.mid")
pattern.make_ticks_abs()
time_resolver = tres.TimeResolver(pattern)
for track in pattern:
    for event in track:
        name = event.name
        tick = event.tick
        milliseconds = time_resolver.tick2ms(tick)
        print(f"event {name} with MIDI tick {tick} happens after {milliseconds} milliseconds.")

