# hows-herg
A website to see how Herg's feeling


## Locally Set Up Project
1. Create a python 3 virtual environment and pip install the requirements.txt
2. Add all necessary bash_profile vars (check constants.py)
3. source ~/.bash_profile
4. source ../[venv_name]/bin/activate
5. python manage.py createsuperuser –username=admin
6. Set up the Twilio webhook for the phone number at api/message_receive
7. Make sure the local env var is set to head.local_settings


## Locally Run Code
1. python manage.py runserver (use --insecure if not using local settings)
2. To test the endpoint: curl -X POST http://localhost:8000/api/message_receive -d '{"body_here": "status"}'
3. ./ngrok http 8000 (use this to test the receive webhook- this serves a temporary site)


## To Deploy Project to Heroku
Heroku set up following instructions here:
https://www.codementor.io/@jamesezechukwu/how-to-deploy-django-app-on-heroku-dtsee04d4

1. git init
2. git add .
3. git commit -m 'commit'
4. git push heroku master


## Heroku Useful Commands
1. heroku logs –tail
2. heroku run python manage.py createsuperuser
3. heroku run python manage.py joey_tribiani_how_you_doin
