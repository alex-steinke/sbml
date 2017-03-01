from nose.tools import assert_equals
from SBMLshort.sbml import Unit, UnitDefinition, Compartment
import json


class TestUnit:
    def setup(self):
        self.my_unit = Unit("kg", -1, 0, 1)

    def teardown(self):
        pass

    def test_init(self):
        assert_equals(self.my_unit.kind, "kg")
        assert_equals(self.my_unit.exponent, -1)
        assert_equals(self.my_unit.scale, 0)
        assert_equals(self.my_unit.multiplier, 1)

    def test_str(self):
        assert_equals(str(self.my_unit), "kg: (10^(0+1))^-1")


class TestUnitDefinition:
    def setup(self):
        self.my_def = UnitDefinition("id", "name")

    def teardown(self):
        pass

    def test_init(self):
        assert_equals(self.my_def.id, "id")
        assert_equals(self.my_def.name, "name")

    def test_dict(self):
        assert_equals({c[0]: c[1] for c in self.my_def.dict()},
                      {"id": "id", "name": "name"})

    def test_to_json(self):
        my_unit = Unit("kg", -1, 0, 1)
        self.my_def.add_unit(my_unit)
        assert_equals(self.my_def.to_json(),
                      json.dumps({"listOfUnits": [{"kind": "kg",
                                                   "exponent": -1,
                                                   "multiplier": 1}],
                                  "id": "id", "name": "name"}))


class TestCompartment:
    def setup(self):
        self.my_comp = Compartment("id", 1, 'name')

    def teardown(self):
        pass

    def test_init(self):
        assert_equals(self.my_comp.to_json(), json.dumps({"constant": 1,
                                                          "id": "id",
                                                          "name": "name"}))
