from django.views.generic import FormView
from forms import NewModelForm, EditModelForm, NewUnitDefinitionForm, \
    EditUnitDefinitionForm, NewUnitForm
from SBMLshort.sbml import Model, UnitDefinition, Unit
from django.forms import Form


class ModelView(FormView):
    template_name = 'index.html'
    success_url = "/"
    form_class = Form
    new_form_class = NewModelForm
    edit_form_class = EditModelForm

    def get_initial(self):
        initial = super(ModelView, self).get_initial()
        if 'model' in self.request.session:
            for input_value in {c[0]: c[1] for c in
                                self.request.session['model'].dict()}.keys():
                initial[input_value] = self.request.session['model'].__dict__[
                    input_value]
        return initial

    def get_context_data(self, **kwargs):
        context = super(ModelView, self).get_context_data(**kwargs)
        context['path'] = self.request.path
        if 'model' in self.request.session:
            context['model'] = self.request.session['model']
            context['form'] = EditModelForm(initial=self.get_initial())
        else:
            context['form'] = NewModelForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'model' in self.request.session:
            form = self.edit_form_class
        else:
            form = self.new_form_class
        return self.form_valid(self.get_form(form))

    def form_valid(self, form):
        str(form)
        if 'model' not in self.request.session:
            self.request.session['model'] = Model(form.cleaned_data['id'])
        else:
            for update in form.cleaned_data.keys():
                setattr(self.request.session['model'], update,
                        form.cleaned_data[update])
        return super(ModelView, self).form_valid(form)


class UnitsView(FormView):
    template_name = 'index.html'
    success_url = "/units"
    form_class = Form
    new_def_form = NewUnitDefinitionForm
    edit_def_form = EditUnitDefinitionForm
    new_unit_form = NewUnitForm

    def get_context_data(self, **kwargs):
        context = super(UnitsView, self).get_context_data(**kwargs)
        context['path'] = self.request.path
        context['model'] = self.request.session['model']
        context['newUnitDef'] = NewUnitDefinitionForm(
            initial={'func': 'newDef'})
        context['newUnit'] = NewUnitForm(initial={'func': 'newUnit'},
                                         choices=((x.id, x.id) for x in
                                                  self.request.session[
                                                      'model'].unitDefinitions))
        if 'editDefID' in self.request.session:
            context['editUnitDef'] = EditUnitDefinitionForm(initial={
                'func': 'saveDef_' + self.request.session['editDefID'],
                'id': self.request.session['editDefID']})
            del self.request.session['editDefID']
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class
        if request.POST['func'] == 'newDef':
            form = self.new_def_form
        elif 'delDef_' in request.POST['func']:
            def_id = request.POST['func'].replace('delDef_', '')
            def_index = request.session['model'].unitDefinitions.index(
                UnitDefinition(def_id))
            request.session['model'].unitDefinitions.pop(def_index)
        elif 'editDef_' in request.POST['func']:
            self.request.session['editDefID'] = request.POST['func'].replace(
                'editDef_', '')
        elif 'saveDef_' in request.POST['func']:
            form = self.edit_def_form
        elif request.POST['func'] == 'newUnit':
            # after get form content of ChoiceField is lost (probably because
            # choices are missing in the field definition) so here is an other workaround
            self.request.session['tmp'] = request.POST['unit_def']
            form = self.new_unit_form
            print 'sdfdsfdf'
        return self.form_valid(self.get_form(form))

    def form_valid(self, form):
        str(form)
        if type(form) == NewUnitDefinitionForm:
            self.request.session['model'].add_unit_def(
                UnitDefinition(form.cleaned_data['id']))
        if type(form) == EditUnitDefinitionForm:
            def_id = self.request.POST['func'].replace('saveDef_', '')
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(def_id))
            setattr(self.request.session['model'].unitDefinitions[def_index],
                    'id', form.cleaned_data['id'])
        if type(form) == NewUnitForm:
            data = form.cleaned_data
            new_unit = Unit(data['kind'], data['exponent'], data['scale'],
                            data['multiplier'])
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(self.request.session.pop('tmp')))
            self.request.session['model'].unitDefinitions[def_index].add_unit(
                new_unit)
        return super(UnitsView, self).form_valid(form)
