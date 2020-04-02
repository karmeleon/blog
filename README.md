# blog

Yep, that's a blog alright!

# Debug run

```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
# init the database
python manage.py migrate --noinput
# Rebuild the database
python manage.py buildsite
# Recompile SCSS
python manage.py compilescss
# Populate static files directory
python manage.py collectstatic --noinput
```

# Deployment

```
./init-letsencrypt.sh
docker-compose up
```