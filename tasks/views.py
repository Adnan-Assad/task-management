from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Count, Max, Min, Avg, Sum

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    context = {
        'names':['Adnan', 'Karim', 'kotha', 'kobita']
       
    }
    return render(request, 'test.html', context)


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()


    if request.method =="POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'task_form.html',{'form': form, 'message':'Task added successfully'} )

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
       "form":  form
    }
    return render(request, "task_form.html", context)
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