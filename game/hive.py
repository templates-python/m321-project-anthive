from dataclasses import dataclass


@dataclass
class Hive:
    """
    an ant hive
    """
    ipaddr: str
    port: int
    xcoord: int
    ycoord: int
    foodstore: int
    color: str
    ants: list

    @property
    def ipaddr(self):
        return self._ipaddr

    @ipaddr.setter
    def ipaddr(self, value):
        self._ipaddr = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def xcoord(self):
        return self._xcoord

    @xcoord.setter
    def xcoord(self, value):
        self._xcoord = value

    @property
    def ycoord(self):
        return self._ycoord

    @ycoord.setter
    def ycoord(self, value):
        self._ycoord = value

    @property
    def foodstore(self):
        return self._foodstore

    @foodstore.setter
    def foodstore(self, value):
        self._foodstore = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def ants(self):
        return self._ants

    @ants.setter
    def ants(self, value):
        self._ants = value
