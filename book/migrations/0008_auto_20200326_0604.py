# Generated by Django 3.0.2 on 2020-03-26 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20200325_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Category',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='librariantemp',
            name='status',
        ),
    ]
