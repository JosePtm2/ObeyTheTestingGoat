# Generated by Django 2.1.7 on 2019-03-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default=None, on_delete='CASCADE', to='lists.List'),
        ),
    ]