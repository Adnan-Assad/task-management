from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task
 


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action:
        assigned_emails = [emp.email for emp in instance.assigned_to.all()
        ]
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task:{instance.title}",
            "adnnn336@gmail.com",
            assigned_emails,
   
)
# post_delete

@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()

        print("Deleted successfully.")