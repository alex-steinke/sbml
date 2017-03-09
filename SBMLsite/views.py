from django.views.generic import FormView
from forms import NewModelForm, EditModelForm, NewUnitDefinitionForm, \
    EditUnitDefinitionForm, NewUnitForm, EditUnitForm, CompartmentForm
from SBMLshort.sbml import Model, UnitDefinition, Unit, Compartment
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
        form = self.get_form(form)
        form.is_valid()
        return self.form_valid(form)

    def form_valid(self, form):
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
    edit_unit_form = EditUnitForm

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
        if 'editUnit' in self.request.session:
            func = self.request.session['editUnit'].split('_')
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(func[1]))
            def_id = self.request.session['model'].unitDefinitions[
                def_index].id
            unit_id = self.request.session['model'].unitDefinitions[
                def_index].listOfUnits.index(Unit(func[2]))
            unit = self.request.session['model'].unitDefinitions[
                def_index].listOfUnits[unit_id]
            unit_data = unit.__dict__
            unit_data['unit_def'] = def_id
            unit_data['func'] = 'saveUnit_' + str(def_id)
            unit_data['old'] = str(unit.kind)
            context['editUnit'] = EditUnitForm(initial=unit_data,
                                               choices=((x.id, x.id) for x in
                                                        self.request.session[
                                                            'model'].unitDefinitions)
                                               )
            del self.request.session['editUnit']
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
        elif 'delUnit_' in request.POST['func']:
            func = request.POST['func'].split('_')
            def_index = request.session['model'].unitDefinitions.index(
                UnitDefinition(func[1]))
            unit_index = request.session['model'].unitDefinitions[
                def_index].listOfUnits.index(Unit(func[2]))
            request.session['model'].unitDefinitions[def_index].del_unit(
                unit_index)
        elif 'editUnit_' in request.POST['func']:
            self.request.session['editUnit'] = request.POST['func']
        elif 'saveUnit_' in request.POST['func']:
            self.request.session['tmp'] = request.POST['unit_def']
            form = self.edit_unit_form
        form = self.get_form(form)
        form.is_valid()
        return self.form_valid(form)

    def form_valid(self, form):
        if type(form) == NewUnitDefinitionForm:
            self.request.session['model'].add_unit_def(
                UnitDefinition(form.cleaned_data['id']))
        elif type(form) == EditUnitDefinitionForm:
            def_id = self.request.POST['func'].replace('saveDef_', '')
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(def_id))
            setattr(self.request.session['model'].unitDefinitions[def_index],
                    'id', form.cleaned_data['id'])
        elif type(form) == NewUnitForm:
            data = form.cleaned_data
            new_unit = Unit(data['kind'], data['exponent'], data['scale'],
                            data['multiplier'])
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(self.request.session.pop('tmp')))
            self.request.session['model'].unitDefinitions[def_index].add_unit(
                new_unit)
        elif type(form) == EditUnitForm:
            def_id = form.cleaned_data['func'].replace('saveUnit_', '')
            def_index = self.request.session['model'].unitDefinitions.index(
                UnitDefinition(def_id))
            unit_index = self.request.session['model'].unitDefinitions[
                def_index].listOfUnits.index(Unit(form.cleaned_data['old']))
            self.request.session['model'].unitDefinitions[
                def_index].del_unit(unit_index)
            new_def_id = self.request.session.pop('tmp')
            new_def_index = self.request.session[
                'model'].unitDefinitions.index(
                UnitDefinition(new_def_id))
            unit = Unit(form.cleaned_data['kind'],
                        form.cleaned_data['exponent'],
                        form.cleaned_data['scale'],
                        form.cleaned_data['multiplier'])
            self.request.session['model'].unitDefinitions[
                new_def_index].add_unit(
                unit)
        return super(UnitsView, self).form_valid(form)


class CompartmentView(FormView):
    template_name = 'index.html'
    success_url = "/compartments"
    form_class = CompartmentForm

    def get_initial(self):
        initial = super(CompartmentView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super(CompartmentView, self).get_context_data(**kwargs)
        context['path'] = self.request.path
        context['model'] = self.request.session['model']
        context['form'] = CompartmentForm(initial={'func': 'new'})
        if 'edit' in self.request.session:
            def_index = self.request.session['model'].compartments.index(
                Compartment(self.request.session.pop('edit')))
            comp = self.request.session['model'].compartments[
                def_index].__dict__
            comp['old'] = comp['id']
            comp['func'] = 'save'
            print comp
            context['edit'] = CompartmentForm(initial=comp)
        return context

    def post(self, request, *args, **kwargs):
        if 'del_' in request.POST['func']:
            def_id = self.request.POST['func'].replace('del_', '')
            def_index = self.request.session['model'].compartments.index(
                Compartment(def_id))
            self.request.session['model'].compartments.pop(def_index)
        elif 'edit_' in request.POST['func']:
            self.request.session['edit'] = request.POST['func'].replace(
                'edit_', '')
        elif request.POST['func'] == 'save':
            print self.request.POST
        form = self.get_form(self.form_class)
        form.is_valid()
        return self.form_valid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        param = {}
        for key, value in data.iteritems():
            if key in Compartment.vars:
                param[key] = value
        if data['func'] == 'new':
            comp = Compartment(**param)
            self.request.session['model'].compartments.append(comp)
        if data['func'] == 'save':
            def_index = self.request.session['model'].compartments.index(
                Compartment(data['old']))
            self.request.session['model'].compartments[
                def_index] = Compartment(**param)
        return super(CompartmentView, self).form_valid(form)
