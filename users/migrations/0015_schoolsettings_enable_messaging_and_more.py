# Generated by Django 5.1.6 on 2025-03-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_idcardtemplate_footer_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsettings',
            name='enable_messaging',
            field=models.BooleanField(default=True, help_text='Enable messaging system across the platform'),
        ),
        migrations.AddField(
            model_name='schoolsettings',
            name='enable_student_to_student_chat',
            field=models.BooleanField(default=True, help_text='Allow students to message other students in their class'),
        ),
        migrations.AddField(
            model_name='student',
            name='chat_enabled',
            field=models.BooleanField(default=True, help_text='If disabled, student cannot send or receive messages (parental control)'),
        ),
    ]
