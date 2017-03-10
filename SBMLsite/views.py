from django.views.generic import FormView
from forms import *
from SBMLshort.sbml import *
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
        if 'gen' in self.request.session:
            context['gen'] = self.request.session['gen']
        if 'model' in self.request.session:
            context['model'] = self.request.session['model']
            context['form'] = EditModelForm(initial=self.get_initial())
        else:
            context['form'] = NewModelForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'model' in self.request.session:
            form = self.edit_form_class
            print self.request.POST
            if 'gen' in self.request.POST:
                print self.request.session['model']
                genstr = str(self.request.session['model'])
                if len(self.request.session['model'].compartments) > 0:
                    genstr = "%s\n@compartments" % genstr
                    for com in self.request.session['model'].compartments:
                        genstr = "%s\n%s" % (genstr, com)
                if len(self.request.session['model'].species) > 0:
                    genstr = "%s\n@species" % genstr
                    for com in self.request.session['model'].species:
                        genstr = "%s\n%s" % (genstr, com)
                if len(self.request.session['model'].parameters) > 0:
                    genstr = "%s\n@parameters" % genstr
                    for com in self.request.session['model'].parameters:
                        genstr = "%s\n%s" % (genstr, com)
                self.request.session['gen'] = genstr
                if len(self.request.session['model'].rules) > 0:
                    genstr = "%s\n@rules" % genstr
                    for com in self.request.session['model'].rules:
                        genstr = "%s\n%s" % (genstr, com)
                if len(self.request.session['model'].reactions) > 0:
                    genstr = "%s\n@reactions" % genstr
                    for com in self.request.session['model'].reactions:
                        genstr = "%s\n%s" % (genstr, com)
                if len(self.request.session['model'].events) > 0:
                    genstr = "%s\n@events" % genstr
                    for com in self.request.session['model'].events:
                        genstr = "%s\n%s" % (genstr, com)
                self.request.session['gen'] = genstr
                form = Form
        else:
            form = self.new_form_class
        form = self.get_form(form)
        form.is_valid()
        return self.form_valid(form)

    def form_valid(self, form):
        if 'model' not in self.request.session:
            self.request.session['model'] = Model(form.cleaned_data['id'])
        else:
            if len(form.cleaned_data.keys()) != 0:
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
        if 'gen' in self.request.session:
            context['gen'] = self.request.session['gen']
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


class DefaultView(FormView):
    template_name = 'index.html'
    form_class = Form
    sbmlclass = None
    type = None
    attr = None

    def get_initial(self):
        initial = super(DefaultView, self).get_initial()
        self.success_url = self.request.path
        if self.request.path == '/compartments':
            self.form_class = CompartmentForm
            self.sbmlclass = Compartment
            self.type = 'Compartment'
            self.attr = 'compartments'
        elif self.request.path == '/parameters':
            self.form_class = ParameterForm
            self.sbmlclass = Parameter
            self.type = 'Parameter'
            self.attr = 'parameters'
        elif self.request.path == '/rules':
            self.form_class = RuleForm
            self.sbmlclass = Rule
            self.type = 'Rule'
            self.attr = 'rules'
        elif self.request.path == '/events':
            self.form_class = EventForm
            self.sbmlclass = Event
            self.type = 'Event'
            self.attr = 'events'
        elif self.request.path == '/species':
            self.form_class = SpeciesForm
            self.sbmlclass = Species
            self.type = 'Species'
            self.attr = 'species'
        elif self.request.path == '/reactions':
            self.form_class = ReactionForm
            self.sbmlclass = Reaction
            self.type = 'Reaction'
            self.attr = 'reactions'
        return initial

    def get_context_data(self, **kwargs):
        context = super(DefaultView, self).get_context_data(**kwargs)
        print self.request.path
        context['path'] = self.request.path
        context['model'] = self.request.session['model']
        context['default'] = self.request.session['model'].__dict__[self.attr]
        context['form'] = self.form_class(initial={'func': 'new'})
        context['type'] = self.type
        if 'gen' in self.request.session:
            context['gen'] = self.request.session['gen']
        if 'edit' in self.request.session:
            def_index = self.request.session['model'].__dict__[
                self.attr].index(
                self.sbmlclass(self.request.session.pop('edit')))
            comp = self.request.session['model'].__dict__[self.attr][
                def_index].__dict__
            comp['old'] = comp['id']
            comp['func'] = 'save'
            context['edit'] = self.form_class(initial=comp)
        return context

    def post(self, request, *args, **kwargs):
        self.get_initial()
        if 'del_' in request.POST['func']:
            def_id = self.request.POST['func'].replace('del_', '')
            def_index = self.request.session['model'].__dict__[
                self.attr].index(
                self.sbmlclass(def_id))
            self.request.session['model'].__dict__[self.attr].pop(def_index)
        elif 'edit_' in request.POST['func']:
            self.request.session['edit'] = request.POST['func'].replace(
                'edit_', '')
        form = self.get_form(self.form_class)
        form.is_valid()
        return self.form_valid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        param = {}
        for key, value in data.iteritems():
            if key in self.sbmlclass.vars:
                param[key] = value
        if data['func'] == 'new':
            comp = self.sbmlclass(**param)
            self.request.session['model'].__dict__[self.attr].append(comp)
        if data['func'] == 'save':
            def_index = self.request.session['model'].__dict__[
                self.attr].index(
                self.sbmlclass(data['old']))
            self.request.session['model'].__dict__[self.attr][
                def_index] = self.sbmlclass(**param)
        return super(DefaultView, self).form_valid(form)
