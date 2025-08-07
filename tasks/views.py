from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Count, Max, Min, Avg, Sum, Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

# create your views here....
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.group.filter(name='Manager').exists()
 
@user_passes_test(is_manager, login_url='no_permission')
def manager_dashboard(request):
     # total_task= Task.objects.all().count()
    # completed_task = Task.objects.filter(status= "COMPLETED").count()
    # in_progress_task = Task.objects.filter(status= "IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status = "PENDING").count()
    # count = {
    #     "total_task":
    #     "completed_task":
    #     "in_progress":
    #     "pending":
    # }
    type = request.GET.get('type', 'all')
    # print(type)
    counts = Task.objects.aggregate(
        total= Count('id'),
        completed = Count('id' , filter = Q(status ='COMPLETED')),
        in_progress = Count('id', filter=Q(status = 'IN_PROGRESS')),
        pending = Count('id', filter=Q(status = 'PENDING')),
        )
    
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status = 'COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()



    context = {
        "tasks": tasks,
        "counts":counts,
        # "total_task": total_task,
        # "completed_task": completed_task,
        # "in_progress_task": in_progress_task,
        # "pending_task": pending_task
    }
    return render(request, "dashboard/manager_dashboard.html", context)
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")
 
@login_required
@permission_required("tasks.add_task", login_url='no_permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm() # for GET ER JONNO


    if request.method =="POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST) # FOR POST ER JONNO
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success( request, "Task Created Successfully")
            return redirect('create_task')

            """For Model Form Data"""

            '''For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to') # list[1 ,3]
            # task = Task.objects.create(title = title, description=description, due_date = due_date)
            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task Added Successfully")


    context = {
       "task_form":  task_form , "task_detail_form": task_detail_form
    }
    return render(request, "task_form.html", context)

'''update task start'''
@login_required
@permission_required("tasks.change_task", login_url='no_permission')
def update_task(request , id):
   
    # employees = Employee.objects.all()
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance= task)
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details) # for GET ER JONNO


    if request.method =="POST":
        task_form = TaskModelForm(request.POST, instance= task)
        task_detail_form = TaskDetailModelForm(request.POST , instance=task.details) # FOR POST ER JONNO
        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail_form.save()
            messages.success( request, "Task Updated Successfully")
            return redirect('update_task', id)

            """For Model Form Data"""

            '''For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to') # list[1 ,3]
            # task = Task.objects.create(title = title, description=description, due_date = due_date)
            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task Added Successfully")


    context = {
       "task_form":  task_form , "task_detail_form": task_detail_form
    }
    return render(request, "task_form.html", context)


@login_required
@permission_required("tasks.delete_task", login_url='no_permission')

def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted successfully")
        return redirect('manager_dashboard')
    else:
        messages.error(request, "Something has Wrong")
        return redirect('manager_dashboard')
         
    
@login_required
@permission_required("tasks.view_task", login_url='no_permission')

def view_task(request):
    # tasks = Task.objects.select_related('details').all()
    # tasks = Task.objects.filter(title__icontains="c")
    # tasks = TaskDetail.objects.exclude(priority="M")
    # tasks = Task.objects.filter(due_date=date.today())
    # tasks = Task.objects.filter(status="PENDING")

    # tasks = Task.objects.all()
    # task_3 = Task.objects.get(id=3)
    # first_task = Task.objects.first()
    # return render(request, 'show_task.html', {"tasks": tasks, "task3": task_3, "first_task": first_task } )
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all() #eta forignkey er jonno
    # tasks = Project.objects.prefetch_related('task_set').all() #eta reverse foreignkey and many to many er jonno
    # task_count = Task.objects.aggregate(num_task=Count('id'))
    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(request, 'show_task.html', {'projects': projects})