### NittanyPath

This project comprises the phase II of the implementation of NittanyPath.
  
Tech Stack: DJANGO Stack
1. Python
2. Django framework
3. HTML, CSS, Bootstrap
4. SQLite

***
####**Files**:
Project settings - /cmpsc431w/cmpsc431w directory

App dir - /cmpsc431w/NittanyPathApp

models.py - contains the information regarding the tables and relations

views.py - contains the backend logic of the project - basically the functionality
of each url


urls.py - maps the url of the website

semplates - dir that contains the html templates of the app

static - dir that contains the static content

***
####**Extra Credit features**:


- Website's UI and frontend
- admin feature
- announcements
***
####**How to run**:

-  Create a virtual env and install the required packages mentioned in requirements.txt

```commandline
pip install -r requirements.txt
```

-  Once the requirements are installed, run the server to start the app

```commandline
python migrate.py runserver
```

****
Sources used:

Login page template - https://bootstrapmade.com/knight-free-bootstrap-theme/?download_theme=knight.zip

Bootstrap Documentation - https://getbootstrap.com/docs/4.0/getting-started/introduction/

Django Documentation - https://docs.djangoproject.com/en/3.0/
