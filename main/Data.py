import math
import cmath
import numpy as np


class Data:
    """
    Class Data handle
    """
    def __init__(self, wave=None, magnitude=None, mask=None, n=32, pm=-1):
        """"
        Init Data
        """
        self.magnitude = None
        self.waves = None
        self.steps = n
        self.pm = pm
        # insert values
        if wave is not None:
            self.add_wave(wave, n=n, pm=pm)
        if magnitude is not None:
            self.add_mag(magnitude)
        if mask is not None:
            self.waves[mask == 0] = None

    @classmethod
    def from_txt(cls, wave_file=None, mag_file=None, mask_file=None, n=32, pm=-1) -> 'Data':
        """

        :param wave_file:
        :param mag_file:
        :param mask_file:
        :param n:
        :param pm:
        :return:
        """
        # import complex-valued wave file
        if wave_file is not None:
            wave = np.genfromtxt(wave_file, delimiter=',', dtype=str)
            wave = np.vectorize(lambda n: np.complex(n.replace('i', 'j')))(wave)

        # import magnitude
        if mag_file is not None:
            magnitude = np.genfromtxt(mag_file, delimiter=',', dtype=float)

        # import mask
        if mask_file is not None:
            mask = np.genfromtxt(mask_file, delimiter=',', dtype=float)

        return cls(wave=wave, magnitude=magnitude, mask=mask, n=n, pm=pm)

    def add_wave(self, data_2d, n=32, pm=-1):
        """

        :param data_2d:
        :param n:
        :param pm:
        :return:
        """
        # check if wave data is complex
        assert np.iscomplex(data_2d).any(), 'Wave data is not complex!'
        assert len(data_2d.shape) == 2, 'Wave data should be 2d!'

        self.steps = n
        self.pm = pm
        self.__animate_wave(data_2d)

    # private
    def __animate_wave(self, wave2d):
        """
        Rotate wave field
        :param n:
        :param pm:
        :return:
        """
        rot = [cmath.exp(complex(ii)) for ii in self.pm * np.linspace(2 * math.pi / self.steps, 2 * math.pi, self.steps) * 1j]
        self.waves = np.array([idx * rot for idx in np.nditer(wave2d)]).reshape((wave2d.shape[0], wave2d.shape[1], self.steps))

    def add_mag(self, data_2d):
        assert len(data_2d.shape) == 2, 'Magnitude data should be 2d!'
        self.magnitude = data_2d

