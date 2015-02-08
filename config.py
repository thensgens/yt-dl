import os

class ConfigProperties(object):

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, v):
        self._output_dir = v

    def __init__(self, output_dir=None):
        if output_dir is not None:
            self._output_dir = output_dir