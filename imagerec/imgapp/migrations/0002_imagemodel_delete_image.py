# Generated by Django 5.0.4 on 2024-04-12 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]