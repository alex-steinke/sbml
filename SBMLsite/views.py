from django.views.generic import FormView, CreateView
from django.contrib import messages
from forms import NewModelForm, EditModelForm
from SBMLshort.sbml import Model
from django.shortcuts import redirect


class IndexView(FormView):
    template_name = 'index.html'
    success_url = "/"
    form_class = NewModelForm
    edit_form_class = EditModelForm

    def get_initial(self):
        initial = super(IndexView, self).get_initial()
        if 'model' in self.request.session:
            for input_value in {c[0]: c[1] for c in
                                self.request.session['model'].dict()}.keys():
                initial[input_value] = self.request.session['model'].__dict__[
                    input_value]
        return initial

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        context['path'] = self.request.path
        if 'model' in self.request.session:
            context['model'] = self.request.session['model']
            context['form'] = EditModelForm(initial=self.get_initial())
        else:
            context['form'] = NewModelForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'model' in self.request.session:
            self.form_class = self.edit_form_class
        return self.form_valid(self.get_form(self.form_class))

    def form_valid(self, form):
        print form
        if 'model' not in self.request.session:
            self.request.session['model'] = Model(form.cleaned_data['id'])
        else:
            for update in form.cleaned_data.keys():
                setattr(self.request.session['model'], update,
                        form.cleaned_data[update])
        return super(IndexView, self).form_valid(form)
