from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Task

@login_required(login_url='accounts:login')
def index(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    remaining_tasks = total_tasks - completed_tasks

    # ✅ progress calculation goes HERE
    progress = 0
    if total_tasks > 0:
        progress = (completed_tasks * 100) // total_tasks

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
        'progress': progress,   # 👈 pass to template
    }

    return render(request, "ToDoApp/index.html", context)


@login_required(login_url='accounts:login')
def add_task(request):
    """Add a new task"""
    if request.method == "POST":
        title = request.POST.get('task', '').strip()
        
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                completed=False
            )
            messages.success(request, 'Task added successfully!')
            return redirect('todoapp:index')
        else:
            messages.error(request, 'Task cannot be empty!')
    
    return redirect('todoapp:index')

@login_required(login_url='accounts:login')
def delete_task(request, task_id):
    """Delete a specific task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('todoapp:index')

@login_required(login_url='accounts:login')
def toggle_task(request, task_id):
    """Toggle task completion status"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('todoapp:index')

@login_required(login_url='accounts:login')
def delete_completed(request):
    """Delete all completed tasks"""
    deleted_count = Task.objects.filter(user=request.user, completed=True).delete()[0]
    messages.success(request, f'{deleted_count} completed task(s) deleted!')
    return redirect('todoapp:index')

 