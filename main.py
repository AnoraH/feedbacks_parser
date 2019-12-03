import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from data.models import *
from data.parsers import FeedbackParser


def main():
    parser = FeedbackParser(
        # True if start headless (without open browser window)
        headless=False,
        # Path to selenium chrome driver
        executable_path='chromedriver.exe',
        # Here we store all data after parsing
        result_dir='result'
    )


if __name__ == '__main__':
    main()
