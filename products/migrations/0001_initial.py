# Generated by Django 4.0.3 on 2022-04-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('goal_amount', models.IntegerField()),
                ('closing_date', models.DateTimeField()),
                ('funding_amount', models.IntegerField()),
            ],
        ),
    ]