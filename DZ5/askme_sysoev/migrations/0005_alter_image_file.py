# Generated by Django 5.1.4 on 2024-12-28 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme_sysoev', '0004_alter_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=''),
        ),
    ]
