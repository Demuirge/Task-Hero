from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Case, When, Value

from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request, 'task_manager/home.html')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(creator=request.user)

    priority_order = Case(
        When(priority='H', then=Value(1)),
        When(priority='M', then=Value(2)),
        When(priority='L', then=Value(3)),
        default=Value(4)
    )

    todo_tasks = tasks.filter(status='TD').order_by(priority_order)
    inprogress_tasks = tasks.filter(status='IP').order_by(priority_order)
    completed_tasks = tasks.filter(status='C').order_by(priority_order)

    context = {
        "tasks": tasks,
       "todo_tasks": todo_tasks,
       "inprogress_tasks": inprogress_tasks,
       "completed_tasks": completed_tasks 
    }

    return render(request, "task_manager/dashboard.html", context)

@login_required
def task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, "task_manager/task.html", {"task": task})

@login_required
def create_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            messages.success(request, "Task created successfully")
            return redirect('Task_Manager:dashboard')
    
    context = {"form": form}
    return render(request, "task_manager/create_task.html", context)

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to edit this task")
        return redirect('Task_Manager:dashboard')
    
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task edited successfully")
            return redirect('Task_Manager:task', task_id)
    
    context = {
        "task": task,
        "form": form    
    }
    return render(request, "task_manager/edit_task.html", context)

@login_required
def confirm_delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to delete this task")
        return redirect('Task_Manager:dashboard')
    
    return render(request, "task_manager/confirm_delete_task.html", {"task": task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.creator:
        messages.error(request, "You do not have permission to delete this task")
        return redirect('Task_Manager:dashboard')
    
    if request.method == "POST":
        task.delete()
        messages.success(request, "You have successfully deleted the task")
        return redirect('Task_Manager:dashboard')
    
    return render(request, "task_manager/dashboard.html", {"task": task})

@require_POST
@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, creator=request.user)
    task.status = 'C'
    task.save()
    return redirect('Task_Manager:task', task_id)