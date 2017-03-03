from nose.tools import assert_equals
from SBMLshort.sbml import *
import json


class TestSbml:
    def setup(self):
        self.my_unit = Unit("kg", -1, 0, 1)
        self.my_def = UnitDefinition("id")
        self.my_comp = Compartment("id", 'name', 1)
        self.my_comp2 = Compartment("id2")
        self.my_spe = Species("id", "cell", 0)
        self.my_spe2 = Species("id", "cell", 0, True, True, True, "test")
        self.my_spe3 = Species("id2", "cell", 0, True, True, True, "test2")
        self.my_param = Parameter("k1", 10)
        self.my_param2 = Parameter("k2", 10, "test", True)
        self.my_rule = Rule("v = 1 + 0.5*t", "assignment")
        self.my_rule2 = Rule("v2=1", "rate")
        self.react = Reaction("r", "Binding", [self.my_spe, self.my_spe3],
                              [self.my_spe3, self.my_spe], "k2*Gene")
        self.react2 = Reaction("rr", "Binding", [self.my_spe3, self.my_spe],
                               [self.my_spe, self.my_spe3], "k2*Gene",
                               [self.my_param, self.my_param2], "TEST")

    def teardown(self):
        pass


class TestUnit(TestSbml):
    def test_init(self):
        assert_equals(self.my_unit.kind, "kg")
        assert_equals(self.my_unit.e, -1)
        assert_equals(self.my_unit.s, 0)
        assert_equals(self.my_unit.m, 1)

    def test_str(self):
        assert_equals(str(self.my_unit), "kg:m=1 e=-1 s=0")


class TestUnitDefinition(TestSbml):
    def test_init(self):
        assert_equals(self.my_def.id, "id")

    def test_dict(self):
        assert_equals({c[0]: c[1] for c in self.my_def.dict()},
                      {"id": "id"})

    def test_str(self):
        self.my_def.add_unit(self.my_unit)
        self.my_def.add_unit(self.my_unit)
        assert_equals(str(self.my_def),
                      " id=kg:m=1 e=-1 s=0; kg:m=1 e=-1 s=0")


class TestCompartment(TestSbml):
    def test_init(self):
        assert_equals(self.my_comp.to_json(), json.dumps({"id": "id",
                                                          "name": "name",
                                                          "size": 1}))

    def test_str(self):
        assert_equals(str(self.my_comp), ' id=1 "name"')
        assert_equals(str(self.my_comp2), ' id2')


class TestSpecies(TestSbml):
    def test_str(self):
        assert_equals(str(self.my_spe), ' cell:id=0 ')
        assert_equals(str(self.my_spe2), ' cell:[id]=0 sbc "test"')


class TestParameter(TestSbml):
    def test_str(self):
        assert_equals(str(self.my_param), ' k1=10')
        assert_equals(str(self.my_param2), ' k2=10v "test"')


class TestRule(TestSbml):
    def test_str(self):
        assert_equals(str(self.my_rule), ' v = 1 + 0.5*t')
        assert_equals(str(self.my_rule2), ' @rate:v2=1')


class TestReaction(TestSbml):
    def test_str(self):
        assert_equals(str(self.react),
                      '@r=Binding\n id+id2 -> id2+id\n k2*Gene')
        assert_equals(str(self.react2),
                      '@rr=Binding "TEST"\n id2+id -> id+id2\n k2*Gene : k1=10,k2=10')
