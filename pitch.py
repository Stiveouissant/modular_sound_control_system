import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import copy
import threading

from PyQt5.QtCore import pyqtSignal, QThread


class PitchRecognition(QThread):
    SAMPLE_FREQ = 48000  # sample frequency in Hz
    WINDOW_SIZE = 48000  # window size of the DFT in samples
    WINDOW_STEP = 12000  # step size of window
    WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ  # length of the window in seconds
    SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ  # length between two samples in seconds
    NUM_HPS = 8  # max number of harmonic product spectrums
    DELTA_FREQ = (SAMPLE_FREQ / WINDOW_SIZE)  # frequency step width of the interpolated DFT
    CONCERT_PITCH = 440
    ALL_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(PitchRecognition, self).__init__(parent=parent)
        self.hann_window = np.hanning(self.WINDOW_SIZE)
        self.window_samples = [0 for _ in range(self.WINDOW_SIZE)]
        self.noteBuffer = ["1", "2", "3"]
        self.recognised_note = ""
        self.stream = None

    def find_closest_note(self, pitch):
        i = int(np.round(np.log2(pitch / self.CONCERT_PITCH) * 12))
        closest_note = self.ALL_NOTES[i % 12] + str(4 + np.sign(i) * int((9 + abs(i)) / 12))
        closest_pitch = self.CONCERT_PITCH * 2 ** (i / 12)
        return closest_note, closest_pitch

    def pitch_callback(self, indata, frames, time, status):
        if status:
            print("status" + str(status))
        if any(indata):
            self.window_samples = np.concatenate((self.window_samples, indata[:, 0]))  # append new samples
            self.window_samples = self.window_samples[len(indata[:, 0]):]  # remove old samples

            signal_power = (np.linalg.norm(self.window_samples, ord=2) ** 2) / len(self.window_samples)
            if signal_power < 5e-7:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Closest note: ...")
                return

            hann_samples = self.window_samples * self.hann_window
            magnitude_spec = abs(scipy.fftpack.fft(hann_samples)[:len(hann_samples) // 2])

            # Supress mains hum
            for i in range(int(62 / self.DELTA_FREQ)):
                magnitude_spec[i] = 0

            # Calculate average energy per frequency for the octave bands
            octave_bands = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
            for j in range(len(octave_bands) - 1):
                ind_start = int(octave_bands[j] / self.DELTA_FREQ)
                ind_end = int(octave_bands[j + 1] / self.DELTA_FREQ)
                ind_end = ind_end if len(magnitude_spec) > ind_end else len(magnitude_spec)
                avg_energy_per_freq = 1 * (np.linalg.norm(magnitude_spec[ind_start:ind_end], ord=2) ** 2) / (ind_end - ind_start)
                avg_energy_per_freq = avg_energy_per_freq ** 0.5
                for i in range(ind_start, ind_end):
                    magnitude_spec[i] = magnitude_spec[i] if magnitude_spec[i] > avg_energy_per_freq else 0  # suppress white noise

            # Interpolate spectrum
            mag_spec_intpol = np.interp(np.arange(0, len(magnitude_spec), 1 / self.NUM_HPS),
                                        np.arange(0, len(magnitude_spec)), magnitude_spec)
            mag_spec_intpol = mag_spec_intpol / np.linalg.norm(mag_spec_intpol, ord=2)  # normalize it

            hps_spec = copy.deepcopy(mag_spec_intpol)

            for i in range(self.NUM_HPS):
                tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_intpol) / (i + 1)))], mag_spec_intpol[::(i + 1)])
                if not any(tmp_hps_spec):
                    break
                hps_spec = tmp_hps_spec

            max_ind = np.argmax(hps_spec)
            max_freq = max_ind * (self.SAMPLE_FREQ / self.WINDOW_SIZE) / self.NUM_HPS

            closest_note, closest_pitch = self.find_closest_note(max_freq)
            max_freq = round(max_freq, 1)
            closest_pitch = round(closest_pitch, 1)

            self.noteBuffer.insert(0, closest_note)  # note that this is a ringbuffer
            self.noteBuffer.pop()

            majority_vote = max(set(self.noteBuffer), key=self.noteBuffer.count)

            if self.noteBuffer.count(majority_vote) > 1:
                detected_note = majority_vote
            else:
                return
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Closest note: {closest_note} {max_freq}/{closest_pitch} and detectednote: {detected_note}")
            self.signal.emit(closest_note)

        else:
            print('no input')

    def create_stream(self):
        print("Starting HPS guitar tuner...")
        self.stream = sd.InputStream(channels=1, callback=self.pitch_callback, blocksize=self.WINDOW_STEP,
                                     samplerate=self.SAMPLE_FREQ)
        self.stream.start()
        return

    def start_stream(self):
        self.background_stream = threading.Thread(target=self.create_stream)
        self.background_stream.start()

    def stop_stream(self):
        self.stream.abort()

    def return_note(self):
        return self.recognised_note
