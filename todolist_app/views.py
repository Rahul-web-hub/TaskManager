from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method=="POST":
        form=TaskForm(request.POST or None)
        if form.is_valid():
           instance= form.save(commit=False)
           instance.manage=request.user
           instance.save()
        messages.success(request,("New Task Added"))
        return redirect('task')
    else:
        all_tasks= TaskList.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'task.html',{'all_tasks':all_tasks})
@login_required
def delete_task(request, task_id):
    try:
        task = get_object_or_404(TaskList, pk=task_id)
        if task.manage==request.user:
            task.delete()
            return redirect('task')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    else:
        messages.error(request,("You are not allowed"))
@login_required
def edit_task(request,task_id):
        if request.method=="POST":
            task = get_object_or_404(TaskList, pk=task_id)
            form=TaskForm(request.POST or None, instance=task)
            if form.is_valid():
                form.save()
            messages.success(request,("Task Edited"))
            return redirect('task')
        else:
            task_obj= TaskList.objects.get(pk=task_id)
            return render(request,'edit.html',{'task_obj':task_obj})
        
@login_required
def complete_task(request, task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,("You are not allowed"))
    
    return redirect('task')
@login_required
def pending_task(request, task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done=False
    task.save()
    
    return redirect('task')
def contact(request):
    context={
        'welcome_text':"welcome to contact page",   
    }
    return render(request,'contact.html',context)
def about(request):
    context={
        'welcome_text':"welcome to about page",   
    }
    return render(request,'about.html',context)
def index(request):
    context={
        'index_text':"welcome to index page",   
    }
    return render(request,'index.html',context)

