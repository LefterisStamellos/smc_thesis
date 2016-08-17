import numpy as np
import pandas as pd
import os
import random

class DrumSounds:

    def __init__(self,X,model,alt_sounds_filenames):
        self.X = X
        self.model = model
        self.alt_sounds_filenames = alt_sounds_filenames

    def drumloops(self,drumloops):

        X = self.X
        model = self.model
        alt_sounds_filenames = self.alt_sounds_filenames

        drumloops_with_wavs = {}

        #drumloop: drumloop+number
        #instruments: list of instruments in drumloop, e.g. ['kick','snare','hihat']
        #music_filename: e.g. 123456.wav

        for (drumloop,instruments) in drumloops.items():
            result = []
            while instruments:
                #pick an instrument at random (more specifically, the row from X containing random instrument's feature values)
                randind = random.randrange(0,len(X))
                randomX = X[randind].reshape(1,-1)

                #predict random instrument's class
                predicted_instrument = model.predict(randomX)[0]

                #if (predicted) class is in instruments (e.g. random instrument's class == hihat and hihat in instruments)
                #remove the instrument from instruments list (i.e. don't look for it again) and detect the sound's filename
                if predicted_instrument in instruments:
                    index = instruments.index(predicted_instrument)
                    instruments.remove(predicted_instrument)
                    alt_sound_filename = alt_sounds_filenames[randind]
                    result.insert(index,(alt_sound_filename[0],predicted_instrument))

            instruments = list(zip(*result)[1])
            drumloops_sound_filenames = list(zip(*result)[0])
            drumloops_with_wavs[drumloop] = (instruments,drumloops_sound_filenames)

        return drumloops_with_wavs


    ############### ask for one instrument, get one or more real and one random alternative ##############
    def one_or_more_real_one_alt(self,instrument,real_instrument_filenames,n_of_real_inst = 1):
        model = self.model
        X = self.X
        alt_sounds_filenames = self.alt_sounds_filenames

        predicted_instrument = []

        while predicted_instrument!=instrument:
            randind = random.randrange(0,len(X)-1)
            randomX = X[randind].reshape(1,-1)

            #predict random instrument's class
            predicted_instrument = model.predict(randomX)[0]

            alt_instrument = alt_sounds_filenames[randind]
        real_instrument = []
        real_instrument = random.sample(real_instrument_filenames,n_of_real_inst)

        return real_instrument,alt_instrument

    ############### ask for one instrument, get 1 real and three random alternative ##############
    def one_real_three_alt(self,instrument,real_instrument_filenames):
        model = self.model
        X = self.X
        alt_sounds_filenames = self.alt_sounds_filenames

        alt_instruments = []

        while (len(alt_instruments) < 3):
            randind = random.randrange(0,len(X)-1)
            randomX = X[randind].reshape(1,-1)

            #predict random instrument's class
            predicted_instrument = model.predict(randomX)[0]

            if predicted_instrument == instrument and predicted_instrument not in alt_instruments:
                alt_sound_filename = alt_sounds_filenames[randind]
                alt_instruments.append(alt_sound_filename[0])

        real_instrument = random.choice(real_instrument_filenames)

        return real_instrument,alt_instruments

    def one_alt(self,instrument):
        model = self.model
        X = self.X
        alt_sounds_filenames = self.alt_sounds_filenames

        predicted_instrument = []
        while predicted_instrument!=instrument:
            randind = random.randrange(0,len(X)-1)
            randomX = X[randind].reshape(1,-1)
            #predict random instrument's class
            predicted_instrument = model.predict(randomX)[0]

        alt_instrument = alt_sounds_filenames[randind][0]

        return alt_instrument

