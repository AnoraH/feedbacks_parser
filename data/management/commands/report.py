from django.core.management.base import BaseCommand

from progressbar import progressbar

from data.models import Feedback
from data.parsers import FeedbackParser


class Command(BaseCommand):
    help = 'Create a report'

    def handle(self, *args, **options):
        result_dir = 'result'
        FeedbackParser.create_data_structure(result_dir=result_dir)
        feedbacks = Feedback.objects.all()

        self.stdout.write('Creating report...')
        for feedback in progressbar(feedbacks):
            if feedback.mark == '0':
                mark = 'neutral'
            elif feedback.mark == '1':
                mark = 'good'
            else:
                mark = 'bad'

            filename = f'{mark}/{FeedbackParser.generator()}.txt'

            try:
                with open(f'{result_dir}/{filename}', 'w+') as f:
                    f.write(feedback.text)
            except UnicodeEncodeError:
                continue

            FeedbackParser.write_json(file_name=filename, mark=feedback.mark,
                                      result_dir=result_dir)

        self.stdout.write(f"""
            good: {feedbacks.filter(mark="1").count()}
            neutral: {feedbacks.filter(mark="0").count()}
            bad: {feedbacks.filter(mark="-1").count()}
        """)
