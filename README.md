# Feedback parser

### Setup database
Change connection information in settings.py

### Parse site and save feedbacks into database
```
python manage.py parse <page count> --headless
```

### Create report about all saved feedbacks
```
python mange.pt report
```