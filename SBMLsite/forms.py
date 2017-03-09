from django.forms import CharField, HiddenInput, Form, ChoiceField


class ModelForm(Form):
    id = CharField(
        label="Model ID",
        max_length=80,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)


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


class NewUnitDefinitionForm(Form):
    id = CharField(
        label="",
        max_length=80,
        required=True
    )
    func = CharField(
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(NewUnitDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'form-control',
                                               'placeholder': 'Unit Definition ID'})


class EditUnitDefinitionForm(Form):
    id = CharField(
        label="",
        max_length=80,
        required=True
    )
    func = CharField(
        widget=HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(EditUnitDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'form-control',
                                               'placeholder': 'Unit Definition ID'})


class NewUnitForm(Form):
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
        # cant't find a way to set choices for ChoiceField from the view
        # so here is a workaround
        if 'choices' in kwargs:
            choices = kwargs.pop("choices")
        else:
            choices = None
        super(NewUnitForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['unit_def'].choices = choices
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})
