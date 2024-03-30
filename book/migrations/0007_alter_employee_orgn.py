# Generated by Django 3.2.16 on 2023-10-12 11:34

from django.db import migrations, models
import djchoices.choices


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_employee_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='orgn',
            field=models.CharField(choices=[('ENE', 'ENERGY'), ('IOT', 'IOT'), ('FIS', 'FINSERV')], max_length=3, validators=[djchoices.choices.ChoicesValidator({'ENE': 'ENERGY', 'FIS': 'FINSERV', 'IOT': 'IOT'})]),
        ),
    ]
