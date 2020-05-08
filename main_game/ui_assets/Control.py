from pygame import *


class Control:

    def __init__(self):
        self.position = Vector2(0, 0)
        self.size = Vector2(0, 0)
        self.name = ""
        self._enabled = True
        self.surface = None

    def refresh(self):
        if self.surface is None:
            raise ValueError('The \"surface\" variable is not correctly set.')

    def get_enabled(self):
        return self._enabled

    def set_enabled(self, enabled):
        if isinstance(enabled, bool):
            self._enabled = enabled
        else:
            raise TypeError('Can only set enabled to a boolean value, that is a \"True\" or a \"False\".')

    @property
    def Rect(self):
        return Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    @Rect.setter
    def Rect(self, rect):
        self.position.x = rect.x
        self.position.y = rect.y
        self.size.x = rect.width
        self.size.y = rect.height

    Enabled = property(get_enabled, set_enabled)
