import pyaudio
import struct
import math

from PyQt5.QtCore import pyqtSignal, QThread


class SoundRecognition(QThread):

    signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(SoundRecognition, self).__init__(parent=parent)

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=2,
                                   rate=44100,
                                   input=True,
                                   frames_per_buffer=int(44100 * 0.03))

        self.hard_tap_threshold = 0.17
        self.light_tap_threshold = 0.1
        self.noise_count = 0
        self.error_count = 0
        self.tap_count = 1
        self.tap_table = []

        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def get_rms(self, block):
        # RMS amplitude is defined as the square root of the
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into
        # a string of 16-bit samples

        # get one short out for each two chars in the string.
        count = len(block) / 2
        format = "%dh" % count
        shorts = struct.unpack(format, block)

        # iterate over the block.
        sum_squares = 0.0
        for sample in shorts:
            # sample is a signed short in +/- 32768.
            # normalize it to 1.0
            n = sample * (1.0 / 32768.0)
            sum_squares += n * n

        return math.sqrt(sum_squares / count)

    def run(self):
        self.exiting = False
        while not self.exiting:
            try:
                block = self.stream.read(int(44100 * 0.5))
            except IOError as e:
                self.error_count += 1
                print("(%d) Error recording: %s" % (self.error_count, e))
                self.noise_count = 0

            rms = self.get_rms(block)
            if rms > self.hard_tap_threshold:
                print(rms)
                print('hard tap! ' + str(self.tap_count))
                self.tap_count += 1
                self.tap_table.append("ht;")
                self.noise_count = 0
            elif rms > self.light_tap_threshold:
                print(rms)
                print('light tap! ' + str(self.tap_count))
                self.tap_count += 1
                self.tap_table.append("lt;")
                self.noise_count = 0
            else:
                self.noise_count += 1

            if self.noise_count >= 25:
                self.tap_table.clear()
                print("Clearing tap table")
                self.noise_count = 0
                self.tap_count = 1

            if len(self.tap_table) >= 3:
                print(self.tap_table)
                self.signal.emit(f'{self.tap_table[0]}{self.tap_table[1]}{self.tap_table[2]}')
                self.tap_table.clear()
                self.tap_count = 1
        return
