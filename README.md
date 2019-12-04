# Feedback parser

### Setup database

1. Create PostgreSQL database
2. Change db connection information in settings.py
3. Apply migrations in database
```
python manage.py migrate
```
#
### Parse site and save feedbacks into database
```
python manage.py parse <page count> --headless
```
* page count - quantity of pages you need to parse, **obviously**
* --headless if you need to run browser headless
#
### Create report about all saved feedbacks
```
python mange.pt report
```