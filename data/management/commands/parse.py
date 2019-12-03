from django.core.management.base import BaseCommand

from data.models import Feedback
from data.parsers import FeedbackParser


class Command(BaseCommand):
    help = 'Parse all data'

    def add_arguments(self, parser):
        parser.add_argument('pages', nargs='+', type=int)
        parser.add_argument(
            '--headless',
            action='store_true',
            help='Parse in headless mode',
            default=False
        )

    def handle(self, *args, **options):
        pages = options['pages'][0]
        headless = options['headless']

        def db_callback(text: str, mark: int):
            try:
                prev = text[:50]
            except IndexError:
                prev = text
            Feedback.objects.update_or_create(preview=prev, text=text, mark=mark)

        parser = FeedbackParser(
            # True if start headless (without open browser window)
            headless=headless,
            # Path to selenium chrome driver
            executable_path='chromedriver.exe',
            # Here we store all data after parsing
            result_dir='result',
            # Callback to work with db
            db_callback=db_callback
        )

        print('Start parsing...')
        parser.run(page_count=pages)
