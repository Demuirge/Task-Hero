from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request, 'task_manager/home.html')

def dashboard(request):
    tasks = Task.objects.all()
    return render(request, "task_manager/dashboard.html", {"tasks": tasks})

def task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, "task_manager/task.html", {"task": task})

def create_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            messages.success(request, "Task created successfully")
            return redirect('task_manager:dashboard')
    
    context = {"form": form}
    return render(request, "task_manager/create_task.html", context)

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to edit this task")
        return redirect('task_manager:dashboard')
    
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task edited successfully")
            return redirect('task_manager:task', task_id)
    
    context = {
        "task": task,
        "form": form    
    }
    return render(request, "task_manager/edit_task.html", context)

def confirm_delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to delete this task")
        return redirect('task_manager:dashboard')
    
    return render(request, "task_manager/confirm_delete_task.html", {"task": task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to delete this task")
        return redirect('task_manager:dashboard')
    
    if request.method == "POST":
        task.delete()
        messages.success(request, "You have successfully deleted the task")
        return redirect('task_manager:dashboard')
    
    return render(request, "task_manager/dashboard.html", {"task": task})

