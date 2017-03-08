import json


class SbmlObject(object):
    def dict(self):
        for attr in self.__dict__:
            if self.__dict__[attr] is not None and self.__dict__[attr] != []:
                yield attr, self.__dict__[attr]

    def to_json(self):
        return json.dumps(self,
                          default=lambda o: {c[0]: c[1] for c in o.dict()})


class Model(SbmlObject):
    def __init__(self, mid, name=None, substance_units=None, time_units=None,
                 volume_units=None, area_units=None, length_units=None,
                 extent_units=None, conversion_factor=None):
        self.id = mid
        self.name = name
        self.substanceUnits = substance_units
        self.timeUnits = time_units
        self.volumeUnits = volume_units
        self.areaUnits = area_units
        self.lengthUnits = length_units
        self.extentUnits = extent_units
        self.conversionFactor = conversion_factor
        self.species = []
        self.parameters = []
        self.rules = []
        self.reactions = []
        self.events = []


class Unit(SbmlObject):
    def __init__(self, kind=None, exponent=None, scale=None, multiplier=None):
        self.kind = kind
        self.e = exponent
        self.s = scale
        self.m = multiplier

    def __str__(self):
        unit_dict = dict(self.dict())
        unit_info = []
        for attr, value in self.dict():
            if attr != 'kind':
                unit_info.append(str(attr) + '=' + str(value))
        return '%s:%s' % (unit_dict['kind'], ' '.join(unit_info))


class UnitDefinition(SbmlObject):
    def __init__(self, udid):
        self.id = udid
        self.listOfUnits = []

    def __str__(self):
        return ' %s=%s' % (self.id, '; '.join(
            [str(unit) for unit in self.listOfUnits]))

    def add_unit(self, unit):
        self.listOfUnits.append(unit)

    def del_unit(self, unit):
        self.listOfUnits.pop(unit)


class Compartment(SbmlObject):
    def __init__(self, compid, name=None, size=None, constant=None):
        self.id = compid
        self.size = size
        self.constant = constant
        self.name = name

    def __str__(self):
        result = ' ' + self.id
        if self.size:
            result = '%s=%s' % (result, self.size)
        if self.name:
            result = '%s "%s"' % (result, self.name)
        return result


class Species(SbmlObject):
    def __init__(self, sid, compartment, initial_amount,
                 has_only_substance_units=False, boundary_condition=False,
                 constant=False, name=None):
        self.id = sid
        self.compartment = compartment
        self.initialAmount = initial_amount
        self.hasOnlySubstanceUnits = has_only_substance_units
        self.boundaryCondition = boundary_condition
        self.constant = constant
        self.name = name

    def __str__(self):
        sid = '[%s]' % self.id if self.constant else self.id
        bool_attr = 's' if self.hasOnlySubstanceUnits else ''
        bool_attr = bool_attr + 'b' if self.boundaryCondition else bool_attr
        bool_attr = bool_attr + 'c' if self.constant else bool_attr
        result = ' %s:%s=%s %s' % (
            self.compartment, sid, self.initialAmount, bool_attr)
        result = '%s "%s"' % (
            result, self.name) if self.name is not None else result
        return result


class Parameter(SbmlObject):
    def __init__(self, pid, value, name=None, constant=False):
        self.id = pid
        self.value = value
        self.name = name
        self.constant = constant

    def __str__(self):
        result = ' %s=%s' % (self.id, self.value)
        result = '%sv' % result if self.constant else result
        result = '%s "%s"' % (
            result, self.name) if self.name is not None else result
        return result


class Rule(SbmlObject):
    def __init__(self, body, ruletype):
        self.body = body
        self.type = ruletype

    def __str__(self):
        if self.type == "rate":
            return ' @rate:%s' % self.body
        else:
            return ' %s' % self.body


class Event(SbmlObject):
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return ' %s' % self.body


class Reaction(SbmlObject):
    def __init__(self, reacttype, rid, reagents, products, body, params=[],
                 name=None):
        self.type = reacttype
        self.reagents = reagents
        self.products = products
        self.params = params
        self.id = rid
        self.name = name
        self.body = body

    def __str__(self):
        reag = '+'.join([r.id for r in self.reagents])
        prod = '+'.join([p.id for p in self.products])
        param = ','.join(
            ['%s=%s' % (param.id, param.value) for param in self.params])
        head = '@%s=%s "%s"' % (self.type, self.id,
                                self.name) if self.name is not None else '@%s=%s' % (
            self.type, self.id)
        result = '%s\n %s -> %s\n %s' % (head, reag, prod, self.body)
        return '%s : %s' % (result, param) if len(param) > 0 else result
