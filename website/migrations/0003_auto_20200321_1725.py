# Generated by Django 2.2.5 on 2020-03-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200321_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_upload',
            field=models.ImageField(upload_to='image'),
        ),
    ]