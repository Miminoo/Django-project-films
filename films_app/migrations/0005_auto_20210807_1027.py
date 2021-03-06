# Generated by Django 3.2.5 on 2021-08-07 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films_app', '0004_auto_20210806_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='rejicer',
            name='birthday_place',
            field=models.CharField(max_length=100, null=True, verbose_name='Место рождения'),
        ),
        migrations.AddField(
            model_name='rejicer',
            name='growth',
            field=models.CharField(max_length=100, null=True, verbose_name='Рост'),
        ),
        migrations.AddField(
            model_name='rejicer',
            name='picture',
            field=models.ImageField(blank=True, upload_to='rejicer/%Y/%m/%d/', verbose_name='Режисёр'),
        ),
    ]
