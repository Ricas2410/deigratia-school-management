# Generated by Django 5.1.6 on 2025-03-06 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('assignment_type', models.CharField(choices=[('HOMEWORK', 'Homework'), ('QUIZ', 'Quiz'), ('TEST', 'Test'), ('EXAM', 'Exam'), ('PROJECT', 'Project')], default='HOMEWORK', max_length=20)),
                ('file_attachment', models.FileField(blank=True, null=True, upload_to='assignments/')),
                ('max_score', models.PositiveIntegerField(default=100)),
                ('due_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_type', models.CharField(choices=[('ASSIGNMENT', 'Assignment'), ('QUIZ', 'Quiz'), ('TEST', 'Test'), ('EXAM', 'Exam'), ('PROJECT', 'Project'), ('TERM', 'Term Grade')], max_length=20)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_score', models.PositiveIntegerField(default=100)),
                ('letter_grade', models.CharField(blank=True, max_length=2, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('term', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice'), ('SHORT', 'Short Answer'), ('LONG', 'Long Answer'), ('FILE', 'File Upload')], max_length=10)),
                ('points', models.PositiveIntegerField(default=1)),
                ('show_feedback', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=20)),
                ('academic_year', models.CharField(max_length=10)),
                ('average_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('teacher_comments', models.TextField(blank=True, null=True)),
                ('days_present', models.PositiveIntegerField(default=0)),
                ('days_absent', models.PositiveIntegerField(default=0)),
                ('days_late', models.PositiveIntegerField(default=0)),
                ('generated_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True, null=True)),
                ('file_answer', models.FileField(blank=True, null=True, upload_to='student_answers/')),
                ('is_correct', models.BooleanField(default=False)),
                ('points_earned', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('file_submission', models.FileField(blank=True, null=True, upload_to='student_submissions/')),
                ('text_submission', models.TextField(blank=True, null=True)),
                ('is_graded', models.BooleanField(default=False)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
