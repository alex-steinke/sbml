FROM python:2.7
RUN apt-get update
RUN apt-get -y remove ipython
RUN apt-get -y install less vim nano ipython
RUN pip install --user matplotlib jupyter pandas mock django teamcity-nose django-bootstrap3
RUN easy_install nose flake8
ADD ./ ./opt/sbml
