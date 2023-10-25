pip install -r requirements.txt

python backend/manage.py makemigrations app
python backend/manage.py migrate

python backend/manage.py runserver