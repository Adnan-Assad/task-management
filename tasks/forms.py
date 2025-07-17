from django import forms
from tasks.models import Task

# Django Form

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250,  label="Task Title")
    description = forms.CharField(widget=forms.Textarea,  label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices= [], label="Assigned To")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", []) # eai employees holo data base er employees
     
        super().__init__( *args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees] # eta k list comphersion bola hoi

# mixing  to apply style to form field
class StyleFormMixin:
    default_classes = "border-2 border-gray-300 w-full rounded-lg shadow-sm focus: border-rose-300 focus: ring-rose-300"
    def apply_styled_widgest(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class':f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300  rounded-lg shadow-sm focus: border-rose-300 focus: ring-rose-300"  

                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

    
# Django Model Form
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    
    
    class Meta:
        model = Task
        fields = ['title','description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

      





        '''Eta holo manual widget'''
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm focus: border-rose-300 focus: ring-rose-300",
        #         'placeholder': 'Enter task title'

        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm resize-none focus: outline-none  focus: border-rose-300 focus: ring-rose-300 rows-5 " ,
        #         'placeholder': 'Describe the task'
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': "border-2 border-gray-300 rounded-lg shadow-sm focus: border-rose-300 focus: ring-rose-300 gap-1",
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #          'class': "space-y-2",
                
        #     }),
            
             
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgest()
