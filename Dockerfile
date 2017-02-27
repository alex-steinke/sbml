FROM python:2.7
RUN apt-get update
RUN apt-get -y remove ipython
RUN apt-get -y install less vim nano ipython
RUN pip install --user pep8 numpy scipy matplotlib jupyter pandas mock teamcity-nose sympy biopython
RUN easy_install nose
RUN git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
ADD ./ ./opt/testing
