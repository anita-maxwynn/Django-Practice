# Model Inheritance

This example demonstrates how to use model inheritance in Django. Model inheritance allows you to create a base model that can be extended by other models, enabling code reuse and a cleaner design.

![alt text](image.png)
## Abstract Base Classes
Abstract base classes are used when you want to define common fields and methods that can be inherited by other models, but you do not want to create a database table for the base class itself. Instead, only the child classes will have their own database tables.
```python
# models.py
from django.db import models
# Model Inheritance Example
class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    joined_date = models.DateField()
    class Meta:
        abstract = True
    
class Student(BaseModel):
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = None  # Overriding the joined_date field to None
class Teacher(BaseModel):
    salary = models.DecimalField(max_digits=10, decimal_places=2)
class Contractor(models.Model):
    payment = models.DecimalField(max_digits=10, decimal_places=2)
```

## Multi-table Inheritance
Multi-table inheritance is used when you want to create a base model that has its own database table, and each child model will also have its own table that includes a foreign key to the base model. This allows you to query the base model and get all related child models.

```python
# models.py
from django.db import models
# Model Inheritance Example
class ExamCenter(models.Model):
    center_name = models.CharField(max_length=100)
    center_city = models.CharField(max_length=100)

class Student(ExamCenter):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
```

## Proxy Models
Proxy models are used when you want to change the behavior of a model without changing its fields or its database table. This is useful for adding custom methods or changing the default ordering of a model.

```python
# models.py
from django.db import models
# Model Inheritance Example
class BaseModel(models.Model):
    name = models.CharField(max_length=100)

class Student(BaseModel):
    class Meta:
        proxy = True
        ordering = ['name']
```

# Model Manager
In Django, a model manager is a class that manages database query operations for a model. It provides methods to retrieve and manipulate data in the database. You can create custom managers to add specific query methods that are not provided by the default manager.
```python
# managers.py
from django.db import models
# Custom Manager Example
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)  # Example filter for active records
    def custom_method(self):
        return self.get_queryset().filter(is_active=True)  # Custom method to filter active records
```

```python
# models.py
from django.db import models
from .managers import CustomManager
# Model Manager Example
class Student(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    objects = CustomManager()
    custom_objects = models.Manager()  # Default manager
```
## Usage
To use the custom manager in your views or other parts of your application, you can call the custom methods defined in the manager. For example:
```python
# views.py
from django.shortcuts import render
from .models import Student
def student_list(request):
    students = Student.objects.custom_method()
    return render(request, 'student_list.html', {'students': students})
def student_active_list(request):
    active_students = Student.custom_objects.filter(is_active=True)
    return render(request, 'active_student_list.html', {'students': active_students})
```

# Model Relationships
Django provides several types of relationships between models, allowing you to define how models are related to each other. The most common types of relationships are:
- One-to-One
- Many-to-One
- Many-to-Many

## One-to-One Relationship
A one-to-one relationship is used when you want to create a unique link between two models.
This is useful for extending a model with additional fields without creating a separate table.
```python
# models.py
from django.db import models
# One-to-One Relationship Example
class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    bio = models.TextField()
    location = models.CharField(max_length=100)
```
> So here, the `Profile` model has a one-to-one relationship with the `User` model, meaning each user can have only one profile and each profile belongs to only one user. So if anything happens(as mentioned ``DELETE``) to `User` object related to `profile` The profile one will also change. but if anything happens with the profile it will not happen in the user.

The behavioural options are ->
- Cascade(will delete both if we try to delete the user)
  - limit_choices_to -> 'is_staff': True (will let further option)
- Protect( Will not let delete if we try to delete the user who has relations with profile)
- Do_Nothing -> literally do nothing, let it happen(*Tame Impala*) well it will cause error if we do not describe any default behaviour

## Many-to-One Relationship
A many-to-one relationship is used when you want to create a link between two models where one model can be related to multiple instances of another model. This is typically done using a foreign key.
```python
# models.py
from django.db import models
# Many-to-One Relationship Example
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

> In this example, the `Book` model has a foreign key to the `Author` model, meaning each book can have only one author, but an author can have multiple books. The `related_name` attribute allows you to access the related books from the author instance.
It has same behavioural options as mentioned above in the one-to-one relationship.

## Many-to-Many Relationship
A many-to-many relationship is used when you want to create a link between two models where each model can be related to multiple instances of the other model. This is typically done using a many-to-many field.
```python
# models.py
from django.db import models
# Many-to-Many Relationship Example
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='courses')
```
> here related name allows you to access the related courses from the student instance. Without it, you would have to use the default related name which is `course_set` for the `Course` model.
```python
# Usage Example
student = Student.objects.get(id=1)
courses = student.courses.all()  # Accessing related courses from the student instance
```

# Context Processors
Context processors are functions that take a request object and return a dictionary of context data that will be added to the context of every template rendered with the request. They are used to make certain data available globally in templates without having to pass it explicitly in every view.
```python
# context_processors.py
def cart_items(request):
    cart_items = request.session.get('cart_items', 0)  # Example: Get cart items from session
    return {'cart_items': cart_items}  # Return a dictionary with the context data
```

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Add your custom context processor here
                'yourapp.context_processors.cart_items',
            ],
        },
    },
]
```
```python
# views.py
from django.shortcuts import render
def home(request):
    return render(request, 'home.html')  # The context processor will automatically add 'cart_items' to the context
```
````
| Use case                               | Why use a context processor?                 |
| -------------------------------------- | -------------------------------------------- |
| 🛒 Cart item count (like your example) | Show cart count in navbar on every page      |
| 👤 Logged-in user profile info         | Display user's name or avatar in header      |
| 🌐 Current site settings               | Site name, footer copyright, etc.            |
| 🔔 Global messages/notifications       | Unread notifications in nav                  |
| 📊 App-wide stats                      | Number of active users, trending posts, etc. |
| 🎨 Theme/branding settings             | Dynamic colors, layout mode                  |
| 🌍 Language or timezone                | For internationalization                     |
````

# Asgi server
ASGI (Asynchronous Server Gateway Interface) is a specification that allows for asynchronous communication between web servers and web applications. It is designed to handle asynchronous protocols like WebSockets, HTTP/2, and HTTP/3, making it suitable for modern web applications that require real-time communication.

## Configuring ASGI in Django
### Daphne
```bash
pip install daphne
```
run the following command to start the ASGI server:
```bash
daphne -p 8000 myproject.asgi:application
```
to run it by runserver command
```python
#settings.py
INSTALLED_APPS = [
    'daphne',
    ...
    
]
...
ASGI_APPLICATION = 'myproject.asgi.application'
```

```bash
python manage.py runserver --asgi
```
### Uvicorn
```bash
pip install uvicorn
```
run the following command to start the ASGI server:
```bash
uvicorn myproject.asgi:application --host=0.0.0.0 --port=8000
```


# Asynchronous Views
Django supports asynchronous views, which allow you to write views that can handle requests asynchronously. This is useful for improving the performance of your application, especially when dealing with I/O-bound operations like database queries or external API calls.

```python
# views.py
from django.http import JsonResponse

async def async_view(request):
    return JsonResponse({'message': 'This is an async view'})
```
> to call http request from server use `httpx` library
```bash
pip install httpx
```
    ```python
    # views.py
    import httpx

    async def async_view(request):
        async with httpx.AsyncClient() as client:
            response = await client.get('https://jsonplaceholder.typicode.com/photos')
        return JsonResponse({'data': response.json()})
    ```

## Example of Asynchronous View
```python
import time
import asyncio
import httpx
from django.http import JsonResponse

async def async_view(request):
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [client.get("https://jsonplaceholder.typicode.com/posts") for _ in range(5)]
        responses = await asyncio.gather(*tasks)

    end_time = time.time()
    time_taken = end_time - start_time

    return JsonResponse({
        'status': 'success',
        'total_request': 5,
        'time_taken': f"{time_taken:.2f} seconds",
        'responses': [response.json() for response in responses]
    })
```
> asyncio is a Python library that provides support for asynchronous programming. It allows you to write concurrent code using the async/await syntax, making it easier to handle I/O-bound operations without blocking the main thread.



# Sync to Async and Async to Sync
Django provides utilities to convert synchronous code to asynchronous and vice versa. This is useful when you need to call synchronous code from an asynchronous context or when you need to call asynchronous code from a synchronous context.

```python
# sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from django.shortcuts import render

def get_data():
    # Synchronous function to get data
    return {'data': 'This is synchronous data'}

async def async_view(request):
    # Convert synchronous function to asynchronous
    data = await sync_to_async(get_data)()
    return render(request, 'async_view.html', {'data': data})

# async_to_sync
async def async_get_data():
    # Asynchronous function to get data
    return {'data': 'This is asynchronous data'}
def sync_view(request):
    # Convert asynchronous function to synchronous
    data = async_to_sync(async_get_data)()
    return render(request, 'sync_view.html', {'data': data})
```
> without defining a helper function we can still use `sync_to_async` and `async_to_sync` directly in the view functions.![alt text](image-1.png)