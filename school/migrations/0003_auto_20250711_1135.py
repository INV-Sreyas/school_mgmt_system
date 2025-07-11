from django.db import migrations

def truncate_models(apps, schema_editor):
    Teacher = apps.get_model('school', 'Teacher')
    Student = apps.get_model('school', 'Student')
    Teacher.objects.all().delete()
    Student.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_student_user_teacher_user'), # 🔁 Replace with actual previous migration
    ]

    operations = [
        migrations.RunPython(truncate_models),
    ]
