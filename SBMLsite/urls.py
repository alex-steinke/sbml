"""SBMLsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from views import ModelView, UnitsView


urlpatterns = [
    url('units', UnitsView.as_view(), name='units'),
    url('compartments', ModelView.as_view(), name='compartments'),
    url('species', ModelView.as_view(), name='species'),
    url('parameters', ModelView.as_view(), name='parameters'),
    url('rules', ModelView.as_view(), name='rules'),
    url('reactions', ModelView.as_view(), name='reactions'),
    url('events', ModelView.as_view(), name='events'),
    url(r'^$', ModelView.as_view(), name='model'),
]
