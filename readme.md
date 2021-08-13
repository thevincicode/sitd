on main path
```
docker-compose up
```

## todo
> should be a migration

 into sitd_web
 ```
docker exec -t -i sitd_web /bin/bash
python manage.py makemigrations sitdapp
python manage.py migrate
```

## create superadmin
```
python manage.py createsuperuser
```

# Develop

```
pip install virtualenvwrapper-win
mkvirtualenv sitdproject
workon sitdproject
pip Install -r requirements.txt
```

if file not found
run:
> convert2Unix.sh


# DataBase Admin
access by the URL : 192.168.99.100:9001

# DataBase

MySql TCP 192.168.99.100: 9002
```
mysql -u root -p -h 192.168.99.100 --port 9002
```

# Site

URL: 192.168.99.100:9000

LICENSE: MIT - Non commercial, until use request, otherwise use as you want.

