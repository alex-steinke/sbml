from django.forms import CharField, HiddenInput, Form, ChoiceField


class ModelForm(Form):
    id = CharField(
        label="Model ID",
        max_length=80,
        required=True,
    )


class NewModelForm(ModelForm):
    id = CharField(
        label="",
        max_length=80,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(NewModelForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'form-control',
                                               'placeholder': 'Model ID'})


class EditModelForm(ModelForm):
    name = CharField(
        label="Name",
        max_length=80,
        required=False
    )
    substanceUnits = CharField(
        label="Substance Units",
        max_length=80,
        required=False
    )
    timeUnits = CharField(
        label="Time Units",
        max_length=80,
        required=False
    )
    volumeUnits = CharField(
        label="Volume Units",
        max_length=80,
        required=False
    )
    areaUnits = CharField(
        label="Area Units",
        max_length=80,
        required=False
    )
    lengthUnits = CharField(
        label="Length Units",
        max_length=80,
        required=False
    )
    extentUnits = CharField(
        label="Extent Units",
        max_length=80,
        required=False
    )
    conversionFactor = CharField(
        label="Conversion Factor",
        max_length=80,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(EditModelForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class UnitDefinitionForm(Form):
    id = CharField(
        label="",
        max_length=80,
        required=True
    )
    func = CharField(
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(UnitDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'form-control',
                                               'placeholder': 'Unit Definition ID'})


class NewUnitDefinitionForm(UnitDefinitionForm):
    def __init__(self, *args, **kwargs):
        super(NewUnitDefinitionForm, self).__init__(*args, **kwargs)


class EditUnitDefinitionForm(UnitDefinitionForm):
    def __init__(self, *args, **kwargs):
        super(EditUnitDefinitionForm, self).__init__(*args, **kwargs)


class UnitForm(Form):
    unit_def = ChoiceField(
        label="Unit Definition",
        required=True
    )
    kind = CharField(
        label="Kind",
        max_length=80,
        required=True
    )
    exponent = CharField(
        label="Exponent",
        max_length=80,
        required=False
    )
    scale = CharField(
        label="Scale",
        max_length=80,
        required=False
    )
    multiplier = CharField(
        label="Multiplier",
        max_length=80,
        required=False
    )
    func = CharField(
        label="",
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        if 'choices' in kwargs:
            choices = kwargs.pop("choices")
        else:
            choices = None
        super(UnitForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['unit_def'].choices = choices
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class NewUnitForm(UnitForm):
    def __init__(self, *args, **kwargs):
        super(NewUnitForm, self).__init__(*args, **kwargs)


class EditUnitForm(UnitForm):
    old = CharField(
        label="",
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(EditUnitForm, self).__init__(*args, **kwargs)


class DefaultForm(Form):
    func = CharField(
        label="",
        widget=HiddenInput()
    )
    old = CharField(
        label="",
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(DefaultForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class CompartmentForm(DefaultForm):
    id = CharField(
        label="Compartment ID",
        max_length=80,
        required=True,
    )
    name = CharField(
        label="Name",
        max_length=80,
        required=False,
    )
    size = CharField(
        label="Size",
        max_length=80,
        required=False,
    )
    constant = CharField(
        label="Constant",
        max_length=80,
        required=False,
    )


class ParameterForm(DefaultForm):
    id = CharField(
        label="Parameter ID",
        max_length=80,
        required=True,
    )
    name = CharField(
        label="Name",
        max_length=80,
        required=False,
    )
    value = CharField(
        label="Value",
        max_length=80,
        required=True,
    )
    constant = CharField(
        label="Constant",
        max_length=80,
        required=False,
    )


class RuleForm(DefaultForm):
    id = CharField(
        label="SBML short rule",
        max_length=80,
        required=True,
    )


class EventForm(DefaultForm):
    id = CharField(
        label="SBML short Event",
        max_length=80,
        required=True,
    )


class SpeciesForm(DefaultForm):
    id = CharField(
        label="Species ID",
        max_length=80,
        required=True,
    )
    compartment = CharField(
        label="Compartment",
        max_length=80,
        required=True,
    )
    initial_amount = CharField(
        label="Initial Amount",
        max_length=80,
        required=True,
    )
    has_only_substance_units = CharField(
        label="Has only substance units (False / True)",
        max_length=80,
        required=False,
    )
    boundary_condition = CharField(
        label="Boundary Condition (False / True)",
        max_length=80,
        required=False,
    )
    constant = CharField(
        label="Constant (False / True)",
        max_length=80,
        required=False,
    )
    name = CharField(
        label="Name",
        max_length=80,
        required=False,
    )


class ReactionForm(DefaultForm):
    id = CharField(
        label="Reaction ID (e.g. r=Conversion)",
        max_length=80,
        required=True,
    )
    body = CharField(
        label="Body",
        max_length=80,
        required=True,
    )
    calc = CharField(
        label="Calculation",
        max_length=80,
        required=True,
    )
    name = CharField(
        label="Name",
        max_length=80,
        required=False,
    )
