README
1.  Introduction
Following application is a Django web page that helps the user to generate
valid SBML short. The main motivation for its development is the difficulty
to produce valid SBML when its write in a text editor.
The program has two main parts a Django application in the package SBMLsite
and a sbml class in the SBMLshort package, which defines classes that could be
used to store and represent a SML short model. Django website provides a set
of forms on different subpages that could be used to create, store and edit
instances of classes defined in SBMLshort. SBMLshort classes are store in a
 file based session using pickling.

2. Development and Version control
During the development, git was used for version control in a local repository
and a remote repository on github (https://github.com/alex-steinke/sbml). I
was using the branching model described in the following article
http://nvie.com/posts/a-successful-git-branching-model/ with main master
branch for release, development branch and multiple feature branches, which
were merged back into development after completion of the feature. The program
was developed in a Docker container and could be deployed using the provided
Dockerfile.  To run the application following command could be used:
docker run -d -p 127.0.0.1:8000:8000 sbml bash -c "python /opt/sbml/manage.py runserver 0.0.0.0:8000"
If the application is installed without Docker some additional python
pakages have to be installed according to the pip install line in the Dockerfile.

3. Testing
For testing, I was using nose testing suite and flake8. Because the program
could be deployed using Docker I was able to run the tests using travis-ci
service after commits. So far only SBMLshort classes were tested.
4. Use
After the installation, the user can access the website and define a new
SBML model, add and change parameters and generate a valid SBML short.
5. To do
Because I run out of time, I had to make a simplified version of Species
and Reactions that could be extended. For example, the user should be able
to pick from existing species and parameter when defining Reactions and from
existing compartments when defining Species. Also testing could be improved
adding Django form tests. Validation could be extended and Views should be
changed so that each view deals just with one type of request, like creation or update.

(References: For design, I was using Bootstrap)

Sry, run out of time, so most of comments are missing.



