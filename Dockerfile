FROM python:2.7
RUN apt-get update
RUN apt-get -y remove ipython
RUN apt-get -y install less vim nano ipython
RUN pip install --user matplotlib jupyter pandas mock teamcity-nose django==1.10.6 django-bootstrap3==8.2.1
RUN easy_install nose flake8
ADD ./ ./opt/sbml
