# Generated by Django 5.1.4 on 2024-12-28 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme_sysoev', '0005_alter_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
