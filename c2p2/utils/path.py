import os.path


__all__ = ('rel',)


rel = lambda p: os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', p)
