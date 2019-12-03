# Generated by Django 3.0 on 2019-12-03 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(unique=True)),
                ('mark', models.CharField(choices=[(1, 'good'), (0, 'neutral'), (-1, 'bad')], max_length=2)),
            ],
        ),
    ]
