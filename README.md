# Social network
In order to activate the project, type the following commands into your terminal (Linux), please:

```shell
git clone https://github.com/dgis-demo/social-network
cd social-network
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd main
python manage.py migrate
python manage.py runserver
```

OR

```shell
git clone https://github.com/dgis-demo/social-network
cd social-network
pipenv install
pipenv shell
cd main
python manage.py migrate
python manage.py runserver
```

The application will be available by the following link:
``http://127.0.0.1:8000/``

On the main page you will be able to find the description of all the API methods.

You can create a superuser and login in django-admin by means of the following commands:
```shell
cd main
python manage.py createsuperuser
```

You can run the automated bot from the root directory `social-network` typing in your terminal such commands:
```shell
cd social-network
python bot.py
```

NOTE: you must be in your python virtual environment (see above, please).