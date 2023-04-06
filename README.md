![Python](https://img.shields.io/badge/Python-3.11.0-3776AB.svg?style=flat-square&logo=Python&logoColor=ffdd54) 
![Django](https://img.shields.io/badge/Django-4.1.7-%23092E20.svg?style=flat-square&logo=django&logoColor=white) 
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=flat-square&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PyCharm](https://img.shields.io/badge/PyCharm-143?style=flat-square&logo=pycharm&logoColor=black&color=black&labelColor=green)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=flat-square&logo=mariadb&logoColor=white)

# danbi-task
단비교육 백엔드 개발 과제

## Setup

The first thing to do is to clone the repository:
```shell
$ git clone https://github.com/yeseong31/danbi-task.git
$ cd danbi-task
```

Create a virtual environment to install dependencies in and activate it:

```shell
$ python -m venv env
$ cd env/Scripts
$ activate
```

Then install the dependencies:

```shell
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. 
This indicates that this terminal session operates in a virtual environment set up by `python env`.

Once `pip` has finished downloading the dependencies,
Create an env file to add the following:

```shell
(env)$ cd project
(env)$ vim .env
```

```shell
# .env
SECRET='Django SECRET KEY'
DB_NAME='Database Table Name'
DB_USER='Database User'
DB_PASSWORD='Database User Password'
DB_HOST='Database Host'
```

Finally, you can run the program by entering the following command:

```shell
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/task/`.
