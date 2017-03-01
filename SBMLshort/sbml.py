import json


class SbmlObject(object):
    def dict(self):
        for attr in self.__dict__:
            if self.__dict__[attr]:
                yield (attr, self.__dict__[attr])

    def to_json(self):
        return json.dumps(self,
                          default=lambda o: {c[0]: c[1] for c in o.dict()})


class Model:
    def __init__(self, name, substance_units, time_units, volume_units,
                 area_units, length_units, extent_units, conversion_factor):
        self.name = name
        self.substanceUnits = substance_units
        self.timeUnits = time_units
        self.volumeUnits = volume_units
        self.areaUnits = area_units
        self.lengthUnits = length_units
        self.extentUnits = extent_units
        self.conversionFactor = conversion_factor


class Unit(SbmlObject):
    def __init__(self, kind, exponent, scale, multiplier):
        self.kind = kind
        self.exponent = exponent
        self.scale = scale
        self.multiplier = multiplier

    def __str__(self):
        return "%s: (10^(%s+%s))^%s" % (self.kind, self.scale,
                                        self.multiplier, self.exponent)


class UnitDefinition(SbmlObject):
    def __init__(self, udid, name=None):
        self.id = udid
        self.name = name
        self.listOfUnits = []

    def add_unit(self, unit):
        self.listOfUnits.append(unit)

    def del_unit(self, unit):
        self.listOfUnits.pop(unit)


class Compartment(SbmlObject):
    def __init__(self, compid, constant, name=None, size=None):
        self.id = compid
        self.size = size
        self.constant = constant
        self.name = name
