import numpy as np

class Generator(object):
    """An event generator"""
    def __init__(self, event_dict):
        self.event_names = event_dict.keys()
        self.event_rates = event_dict.values()
        self.times = np.zeros(len(event_dict))
        for i, event_rate in enumerate(self.event_rates):
            self.times[i] = np.random.exponential(event_rate)

    def draw_event(self):
        ind = self.times.argmin()
        elapsed = self.times[ind]
        self.times = self.times - self.times[ind]
        self.times[ind] = np.random.exponential(self.event_rates[ind])
        return self.event_names[ind], elapsed

if __name__ == "__main__":
    event_dict = {'E1': 12., 'E2': .03}
    gen = Generator(event_dict)
    for i in xrange(1000):
        print gen.draw_event()
