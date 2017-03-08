from django import forms


class ModelForm(forms.Form):
    id = forms.CharField(
        label="Model ID",
        max_length=80,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)


class NewModelForm(ModelForm):
    id = forms.CharField(
        label="",
        max_length=80,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(NewModelForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'form-control',
                                               'placeholder': 'Model ID'})


class EditModelForm(ModelForm):
    name = forms.CharField(
        label="Name",
        max_length=80,
        required=False
    )
    substanceUnits = forms.CharField(
        label="Substance Units",
        max_length=80,
        required=False
    )
    timeUnits = forms.CharField(
        label="Time Units",
        max_length=80,
        required=False
    )
    volumeUnits = forms.CharField(
        label="Volume Units",
        max_length=80,
        required=False
    )
    areaUnits = forms.CharField(
        label="Area Units",
        max_length=80,
        required=False
    )
    lengthUnits = forms.CharField(
        label="Length Units",
        max_length=80,
        required=False
    )
    extentUnits = forms.CharField(
        label="Extent Units",
        max_length=80,
        required=False
    )
    conversionFactor = forms.CharField(
        label="Conversion Factor",
        max_length=80,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(EditModelForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})
