FROM python:2.7
RUN apt-get update
RUN apt-get -y remove ipython
RUN apt-get -y install less vim nano ipython
RUN pip install --user pep8 numpy scipy matplotlib jupyter pandas mock django teamcity-nose sympy biopython
RUN easy_install nose flake8
ADD ./ ./opt/sbml
