from django.http import HttpResponse
from django.template import loader
from SBMLshort.sbml import UnitDefinition, Unit


def index(request):
    template = loader.get_template('index.html')
    print(request.session['test'].__dict__)
    print(request.session['test'].to_json())
    context = {
        'tests': "TEST",
    }
    return HttpResponse(template.render(context, request))


def test(request):
    template = loader.get_template('index.html')
    unit = Unit('test', -1, 0, 1)
    ud = UnitDefinition("id")
    ud.add_unit(unit)
    request.session['test'] = ud
    context = {
        'tests': "TEST",
    }
    return HttpResponse(template.render(context, request))
