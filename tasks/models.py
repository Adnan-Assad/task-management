from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name 
        



class Task(models.Model):
    STATUS_CHOICES =[
        ('PENDING' , 'pending'),
        ('IN_PROGRESS' , 'in progress'),
        ('COMPLETED', 'completed')
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1 )

    assigned_to = models.ManyToManyField(Employee)

                                                
    title = models.CharField(max_length=200)    #Task and TaskDetail one to one Relationship
                                                 # Project and Task Many to one Relationship
                                                 # Employee and Task Many to Many relationship
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices= STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS =(

        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE , related_name="details")


    # assigned_to = models.CharField(max_length=150)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detail form Task {self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name 
