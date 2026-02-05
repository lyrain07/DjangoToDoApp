import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CRUDApp.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from ToDoApp.models import Task

User = get_user_model()
user, created = User.objects.get_or_create(username='johndoe',
                                            defaults={'email':'john@example.com','first_name':'John','last_name':'Doe'})
if created:
    user.set_password('Password123')
    user.save()

# Create tasks
Task.objects.get_or_create(user=user, title='Buy groceries')
Task.objects.get_or_create(user=user, title='Pay bills',)
# Mark 'Pay bills' completed
pay = Task.objects.filter(user=user, title='Pay bills').first()
if pay and not pay.completed:
    pay.completed = True
    pay.save()

# Print summary
qs = Task.objects.filter(user=user)
print('user_created', created)
print('tasks_count', qs.count())
for t in qs:
    print(t.id, t.title, t.completed, t.created_at)
