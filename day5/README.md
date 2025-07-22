## ✅ Django ModelForm Template

```python
from django import forms
from .models import <ModelName>

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = <ModelName>
        fields = ['<field1>', '<field2>']  # List of field names

        labels = {
            '<field_name>': 'Label you want to display',
        }

        error_messages = {
            '<field_name>': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid value.',
            }
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'your-css-class',
                'placeholder': 'Your Placeholder'
            }),
        }
```

---

## 📌 Notes

* The **form fields' data types** are automatically inferred from the model fields.
* For special fields:

  * `ForeignKey` → `ModelChoiceField`
  * `ManyToManyField` → `ModelMultipleChoiceField`

---

## 🧬 Form Inheritance

You can inherit from an existing form like this:

```python
class NewForm(OldForm):
    # Add or override fields here
```

---

## 🔍 Filtering Querysets in Forms


```markdown
packagename/
├── __init__.py       # Declare it as a package
├── customfilter.py   # Your custom filters go here
```
> customfilter.py
```python
from django import templates
register =template.Libarry()
def myreplace(value,arg):
    return value.replace(arg ,'rplacing this word')
register.filter('customfiltername',myreplace)
```

```html
{% load python_file_name %} # at the top of the file
{{data|customfiltername}}
```

![alt text](image.png)


## Dynamic Url


in the url file

```python
from django.urls import path
from . import views

urlpatterns = [
    path('dynamic/<int:pk>/', views.func_name, name='dynamic')
]
```

```python
from django.shortcuts import render

def func_name(request, pk):
    return render(request, 'htmlpage.html', {'pk_value': pk})
```


# Message

It is used at the time of debug and development
at the time of production it is removed

```python
from django.shortcuts import render
from django.contrib import messages
def home (request):
    messages.add_message(request,messages.SUCCESS,'your custom message')
    return render(request, 'student/home.html')

def registration (request):
    return render(request, 'student/registration.html')
```

![Messages](image-1.png)

> *#Disclaimer:-* Debug is usually set at level 10 and the default level is at 20 that's why it's doesn't show up at first
> That's why we have to set it by `messages.set_level(request,messages.DEBUG)`

![](image-2.png) 
>settings.py
We can have custom tags too
for css purposes
