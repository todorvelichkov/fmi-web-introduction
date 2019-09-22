# Introduction to Django


## Installation
```
    # First we need pip
    sudo apt install python3-venv python3-pip

    # Check versions
    pip -V

    # Install virtual envs
    sudo pip install virtualenv

    # Install virtualenvwrapper
    sudo pip install virtualenvwrapper

    # Configure virtualenvwrapper
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    # Could be in: ~/.local/bin/virtualenvwrapper.sh
    source /usr/local/bin/virtualenvwrapper.sh

    # Create virtual env for the project
    mkvirtualenv simple-project

    # other commands
    lsvirtualenv
    workon simple-project
    deactivate
    rmvirtualenv simple-project

    # Now install django into the virutual env
    pip install django

    # test the installation
    python -m django --version

    # check all installed into the virual env
    pip freeze
```

## Starting a New Project
```
    cd ~/projects
    django-admin startproject simple_project
    cd simple_project
```

## The project file structure
```
simple_project/
├── manage.py
└── simple_project
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

- `simple_project/` - The outer `simple_project/` root directory is just a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.

- `manage.py` - A command-line utility that lets you interact with this project in various ways (outside of the request/response life-cycle (e.g. running test)).

- The inner `simple_project/` directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. `simple_project.urls`).

- `simple_project/__init__.py`: An empty file that tells Python that this directory should be considered a Python package.

- `simple_project/settings.py`: Settings/configuration for this  project

- `simple_project/urls.py`: The URL declarations for this project; a “table of contents” of your Django-powered site

- `simple_project/wsgi.py`: An entry-point for WSGI-compatible web servers to serve your project. 
    
    > **WSGI** is the Web Server Gateway Interface. It is a specification that describes how a web server communicates with web applications, and how web applications can be chained together to process one request. **WSGI** is a Python standard described in detail in PEP 3333.


## Run Server
```
    # and open http://127.0.0.1:8000/
    python manage.py runserver
```

## Django documentation

Can be found at: https://docs.djangoproject.com

### How the documentation is organized

- **Tutorials** take you by the hand through a series of steps to create a Web application. Start here if you’re new to Django or Web application development. Also look at the “First steps” below.
-  **Topic guides** discuss key topics and concepts at a fairly high level and provide useful background information and explanation.
- **Reference guides** contain technical reference for APIs and other aspects of Django’s machinery. They describe how it works and how to use it but assume that you have a basic understanding of key concepts.
- **How-to guides** are recipes. They guide you through the steps involved in addressing key problems and use-cases. They are more advanced than tutorials and assume some knowledge of how Django works.