import numpy as np

class photband(object):
    '''
    The Photometric band object
    '''
    def __init__(self):
        '''
        Initialize object
        '''
        self._name    = 'empty'
        self._upcut   = -np.inf
        self._lowcut  = np.inf
        self._xmagerr = None
        self._ymagerr = None
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def upcut(self):
        return self._upcut
        
    @upcut.setter
    def upcut(self, new_upcut):
        self._upcut = new_upcut

    @property
    def lowcut(self):
        return self._lowcut
        
    @lowcut.setter
    def lowcut(self, new_lowcut):
        self._lowcut = new_lowcut

    @property
    def xmagerr(self):
        return self._xmagerr
        
    @xmagerr.setter
    def xmagerr(self, new_xmagerr):
        self._xmagerr = new_xmagerr

    @property
    def ymagerr(self):
        return self._ymagerr
        
    @ymagerr.setter
    def ymagerr(self, new_ymagerr):
        self._ymagerr = new_ymagerr



