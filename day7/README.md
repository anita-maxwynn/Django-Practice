# Signals

In Django, signals are a way to allow certain senders to notify a set of receivers when some action has taken place.

It has many types of signals. They are ->
## Model Signals
- `pre_save`: Sent just before a model's `save()` method is called.
- `post_save`: Sent just after a model's `save()` method is called.
- `pre_delete`: Sent just before a model's `delete()` method is called.
- `post_delete`: Sent just after a model's `delete()` method is called.
- `pre_init`: Sent just before a model's `__init__()` method is called.
- `post_init`: Sent just after a model's `__init__()` method is called.
- `class_prepared`: Sent when a model class is prepared.

## DB Signals
- `connection_created`: Sent when a new database connection is created.
- `connection_closed`: Sent when a database connection is closed.
## Request/Response Signals
- `request_started`: Sent when a request is started.
- `request_finished`: Sent when a request is finished.
- `got_request_exception`: Sent when an exception is raised during request processing.
## User Signals
- `user_logged_in`: Sent when a user logs in.
- `user_logged_out`: Sent when a user logs out.
- `user_password_changed`: Sent when a user changes their password.
- `user_login_failed`: Sent when a user login attempt fails.
## Migration Signals
- `pre_migrate`: Sent before a migration is applied.
- `post_migrate`: Sent after a migration is applied.
## Settings Signals
- `setting_changed`: Sent when a setting is changed.
- `template_rendered`: Sent when a template is rendered.
## Many-to-Many Signals
- `m2m_changed`: Sent when a many-to-many relationship is changed.
## Custom Signals
- You can create custom signals using Django's `Signal` class.


## User Signals Example
Let's see how to use user signals 

```python
# signals.py
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


def login_success(sender,request, user, **kwargs):
    print(f"User {user.username} logged in successfully.")


user_logged_in.connect(login_success,sender=User)

```
we can also use decorators to connect signals:
```python
# signals.py
... #same headers as above
from django.dispatch import receiver

@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    print(f"User {user.username} logged in successfully.")
```
> same work flow with user_logged_out, user_login_failed, etc.

## Model Signals Example
Let's see how to use model signals

```python
# signals.py
from django.db.models.signals import pre_save, post_save,pre_delete, post_delete,pre_init, post_init, class_prepared,pre_migrate, post_migrate
from django.dispatch import receiver

@receiver(pre_save, sender=MyModel)
def my_model_pre_save(sender, instance, **kwargs):
    print(f"About to save {instance} of type {sender.__name__}")

@receiver(post_save, sender=MyModel)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Created new {instance} of type {sender.__name__}")
    else:
        print(f"Updated {instance} of type {sender.__name__}")

@receiver(pre_delete, sender=MyModel)
def my_model_pre_delete(sender, instance, **kwargs):
    print(f"About to delete {instance} of type {sender.__name__}")

@receiver(post_delete, sender=MyModel)
def my_model_post_delete(sender, instance, **kwargs):
    print(f"Deleted {instance} of type {sender.__name__}")

@receiver(pre_init, sender=MyModel)
def my_model_pre_init(sender, *args, **kwargs):
    print(f"About to initialize {sender.__name__}")

@receiver(post_init, sender=MyModel)
def my_model_post_init(sender, instance, **kwargs):
    print(f"Initialized {instance} of type {sender.__name__}")

@receiver(class_prepared, sender=MyModel)
def my_model_class_prepared(sender, **kwargs):
    print(f"Class {sender.__name__} is prepared")

@receiver(pre_migrate)
def my_model_pre_migrate(sender, **kwargs):
    print("About to apply migrations")

@receiver(post_migrate)
def my_model_post_migrate(sender, **kwargs):
    print("Migrations applied successfully")
```

## Request Signals Example
Let's see how to use request signals

```python
# signals.py
from django.core.signals import request_started, request_finished, got_request_exception
from django.dispatch import receiver

@receiver(request_started)
def request_started_handler(sender, **kwargs):
    print("Request has started")

@receiver(request_finished)
def request_finished_handler(sender, **kwargs):
    print("Request has finished")

@receiver(got_request_exception)
def got_request_exception_handler(sender, request, **kwargs):
    print(f"An exception occurred during request processing: {kwargs.get('exception')}")
```

## DB Signals Example
Let's see how to use DB signals
```python
# signals.py
from django.db.backends.signals import connection_created

from django.dispatch import receiver
@receiver(connection_created)
def connection_created_handler(sender, connection, **kwargs):
    print(f"New database connection created: {connection.alias}")
```



## Custom Signals Example
You can create custom signals using Django's `Signal` class.

```python
# signals.py
from django.dispatch import Signal, receiver

# Define a custom signal

notification_sent = Signal()

@receiver(notification_sent)
def send_notification(sender, **kwargs):
    # Logic to send notification
    print("Notification sent!")
    print(f"Sender: {sender}, kwargs: {kwargs}")
```
```python
# views.py
from myapp.signals import notification_sent
def some_view(request):
    # Some logic
    notification_sent.send(sender=request.user, message="Hello, World!")
```

## How to Register Signals

```python
# apps.py
from django.apps import AppConfig
class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        import myapp.signals  # Import the signals module to ensure signals are registered
```


```python
# __init__.py
default_app_config = 'myapp.apps.MyAppConfig'
```
if u do not want to use __init__.py, you can add the app config directly in the settings.py file:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'myapp.apps.MyAppConfig',  # in place of 'myapp'
    ...
]
```



## Caution
- Signals are great for decoupling logic (e.g., don't clutter your views),

- But overusing signals can make your codebase hard to debug and hard to follow, since logic is triggered “in the background.”

### uses of signals
Signals are triggered when specific actions/events happen, especially in the models/auth layer. They're perfect for adding side effects without cluttering your main code.

1. Send Emails or Notifications
    Send a welcome email when a user registers (post_save on User).

    Alert admin when an important model is updated.

```python
@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail("Welcome!", "Thanks for joining.", to=[instance.email])
```
👥 2. Auto-create Related Models
    Automatically create a Profile when a new User is created.

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```
3. Clean Up Data
    When an object is deleted (post_delete), remove associated files or records.

4. Auth Tracking
    Log user login/logout events.

    Trigger actions when login fails.

```python
@receiver(user_logged_in)
def track_login(sender, user, request, **kwargs):
    print(f"{user.username} just logged in")
```
5. Testing & Development
    Mock or track actions during automated tests.

    Reset data when migrations are run (post_migrate).



# Middlewares
Middlewares are a way to process requests globally before they reach the view or after the view has processed them. They can be used for various purposes such as logging, authentication, and more.

> Middleware works for all requests, not just specific ones. It is applied to every request that comes into the Django application.(Womp womp😭)

```markdown
| Feature          | **Middleware**                                   |
| ---------------- | ------------------------------------------------ |
| **Layer**        | HTTP Request/Response cycle                      |
| **Trigger**      | Every request/response                           |
| **Scope**        | Global (affects all views/requests)              |
| **Manual Call?** | Never called manually (auto-applied by Django)   |
| **Best For**     | Security, logging, request/response modification |

| Feature          | **Signals**                                              |
| ---------------- |
| **Layer**        | Model or App event layer (database, login, etc.)         |
| **Trigger**      | Specific events like `post_save`, `user_logged_in`, etc. |
| **Scope**        | Local to models or specific actions                      |
| **Manual Call?** | Also automatic, but must be explicitly connected         |
| **Best For**     | Side effects: emails, logging, cleanup, notifications    |


| Role                  | Middleware                        | Signals                                                    |
| --------------------- | --------------------------------- | ---------------------------------------------------------- |
| Like a **toll booth** | Checks/modifies **every request** | Like a **doorbell** — only rings when an **event happens** |
```

## functional middleware example

```python 
# middlewares.py
def my_fun_middleware(get_response):
    print("One-time configuration or initialization.")
    def middleware(request):
        # Code to be executed for each request before the view (and later middleware) are called.
        print("Before the view")

        response = get_response(request)

        # Code to be executed for each request/response after the view is called.
        print("After the view")
        
        return response

    return middleware
```

```python
# settings.py
MIDDLEWARE = [
    ...
    'myapp.middlewares.my_fun_middleware',  # Add your middleware here
    ...
]
```
We can also use it for rendering templates, for example:
```python
# middlewares.py
from django.shortcuts import render
def template_rendering_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        
        if response.status_code == 200 and 'text/html' in response['Content-Type']:
            # Render a template for the response
            return render(request, 'my_template.html', context={'data': 'Hello, World!'})
        
        return response

    return middleware
```
in this case, the logic in views.py will not be executed, and the template will be rendered directly from the middleware.

## Class-based middleware example

```python
# middlewares.py
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("One-time configuration or initialization.")

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        print("Before the view")

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        print("After the view")
        
        return response
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Code to be executed before the view is called.
        print("Processing view")
        return None  # Return None to continue processing the view
    def process_exception(self, request, exception):
        # Code to handle exceptions raised by the view.
        print(f"Exception occurred: {exception}")
        return None  # Return None to continue processing the exception
    def process_template_response(self, request, response):
        # Code to modify the response before rendering the template.
        print("Processing template response")
        response.context_data['additional_data'] = 'Some additional data'
        return response  # Return the modified response
```

```python
# settings.py
MIDDLEWARE = [
    ...
    'myapp.middlewares.MyMiddleware',  # Add your middleware here
    ...
]
```
### Uses of Middleware
Middleware sits between the request and the view, and between the view and the response. It’s ideal for things that apply to every request or every response.

1. Security
Block users from specific IPs or user agents.

Enforce HTTPS (redirect HTTP to HTTPS).

Add security headers (like X-Frame-Options, Content-Security-Policy).

```python
class BlockIPMiddleware:
    def __call__(self, request):
        if request.META['REMOTE_ADDR'] in ['192.168.1.1']:
            return HttpResponseForbidden("Blocked")
```
2. Logging & Debugging
    Log every incoming request and outgoing response.

    Track performance or API usage stats.

3. Request/Response Modification
    Automatically add headers or cookies.

    Attach metadata or custom attributes to the request before it hits your view.

4. Session & Authentication
    Custom middleware for session-based access control.

    Inject user data globally into all views.

> The order of middleware matters! Django processes them in the order they are listed in `MIDDLEWARE` setting. If one middleware modifies the request, the next one will see that modification.

The oder is like this:
```markdown
Middleware1(init) -> Middleware2(init) -> Middleware1(call) -> Middleware2(call) -> View -> Middleware2(response) -> Middleware1(response)
```

Although you can still make it accessable to speciied users only, by checking the request.user in the middleware:
```python
# middlewares.py
from django.http import HttpResponseForbidden
class UserSpecificMiddleware:
    def __call__(self, request):
        if request.user.is_staff:
            return self.get_response(request)
        else:
            return render(request, 'not_allowed.html')
```
We can also use some restricted key by which anyone can access the site like this:
```python
# middlewares.py
from django.http import HttpResponseForbidden
from django.conf import settings
class RestrictedAccessMiddleware:
    def __call__(self, request):
        unk = "key" # replace with your key
        if 'u' in request.GET and request.GET['u'] == unk:
            return self.get_response(request)
        else:
            return render(request, 'not_allowed.html')
```
The user can access the site by using the key like this:
```http://example.com/?u=key```




# QuerySet

get all:- Modelname.objects.all()
all data but filtered :- ModelName.objects.filter(field=value)
get one object:- ModelName.objects.get(field=value)
get one object or return None:- ModelName.objects.filter(field=value).first()
exclude :- ModelName.objects.exclude(field=value)
count :- ModelName.objects.count()
order by :- ModelName.objects.order_by('field') # ascending
order by descending :- ModelName.objects.order_by('-field')
random :- ModelName.objects.order_by('?')
distinct :- ModelName.objects.distinct()
upto some number of objects :- ModelName.objects.order_by('field')[:10]
to get only some fields :- ModelName.objects.values('field1', 'field2')

to see the SQL query generated by a queryset, you can use the `query` attribute:

```python
queryset = ModelName.objects.filter(field=value)
print(queryset.query)
```


union of two querysets:
```python
queryset1 = ModelName.objects.filter(field1=value1)
queryset2 = ModelName.objects.filter(field2=value2)
combined_queryset = queryset1.union(queryset2)
# to allow duplicates
combined_queryset = queryset1.union(queryset2, all=True)
```
intersection of two querysets:
```python
queryset1 = ModelName.objects.filter(field1=value1) 
queryset2 = ModelName.objects.filter(field2=value2)
intersection_queryset = queryset1.intersection(queryset2)
```
difference of two querysets:
```python
queryset1 = ModelName.objects.filter(field1=value1)
queryset2 = ModelName.objects.filter(field2=value2)
difference_queryset = queryset1.difference(queryset2)
```

`And` and `Or` operations:
```python
# AND operation
queryset = ModelName.objects.filter(field1=value1) & ModelName.objects.filter(field2=value2)
queryset = ModelName.objects.filter(field1=value1,field2=value2)

# OR operation
queryset = ModelName.objects.filter(field1=value1) | ModelName.objects.filter(field2=value2)
```

>get might get multiple objects if the filter is not unique, causing an error, so use it with caution.

first and last:
```python
first_object = ModelName.objects.first()  # Get the first object
last_object = ModelName.objects.last()    # Get the last object
```

we can also do it with other querysets:
```python
first_object = ModelName.objects.filter(field=value).first()  # Get the first object matching the filter
object_2 = ModelName.objects.order_by('field').last()  # Get the last object ordered by 'field'
```
**latest**
```python
latest_object = ModelName.objects.latest('pass_date')
```
> **Note:** `latest()` requires a field to order by, typically a date or timestamp field. in this case, it is `pass_date`. the model must have a field somthing like this`pass_date = models.DateTimeField(auto_now_add=True)`

**earliest**
```python
earliest_object = ModelName.objects.earliest('pass_date')
```
> **Note:** `earliest()` also requires a field to order by, similar to `latest()`. it is `pass_date` in this case.

**Create Data**
```python
# Create a new object
new_object = ModelName.objects.create(field1=value1, field2=value2)
```
> This will create a new object in the database and return the created object.

**get_or_create**
```python
# Get an object if it exists, otherwise create it
obj, created = ModelName.objects.get_or_create(field1=value1, defaults={'field2': value2})
```
> `get_or_create` returns a tuple of the object and a boolean indicating whether it was created or not. The `defaults` argument allows you to specify additional fields to set if the object is created.

**update**
```python
# Update existing objects
ModelName.objects.filter(field1=value1).update(field2=value2)
```
> This will update all objects matching the filter with the new value for `field2`.

**bulk_create**
```python
# Bulk create multiple objects
objects_to_create = [
    ModelName(field1=value1, field2=value2),
    ModelName(field1=value3, field2=value4),
]
ModelName.objects.bulk_create(objects_to_create)
```
> `bulk_create` allows you to create multiple objects in a single query, which is more efficient than creating them one by one.


## Field lookups
Django provides a powerful way to filter querysets using field lookups. These lookups allow you to perform various types of queries on your models. Here are some common field lookups:
- exact: Matches the exact value.
```python
ModelName.objects.filter(field__exact=value)
```
- iexact: Case-insensitive exact match.
```python
ModelName.objects.filter(field__iexact=value)
```
- contains: Checks if the field contains the specified value.
```python
ModelName.objects.filter(field__contains=value)
```
- icontains: Case-insensitive contains check.
```python
ModelName.objects.filter(field__icontains=value)
```
- in: Checks if the field's value is in a list of values.
```python
ModelName.objects.filter(field__in=[value1, value2, value3])
```
- gt: Greater than.
```python
ModelName.objects.filter(field__gt=value)
```
- gte: Greater than or equal to.
```python
ModelName.objects.filter(field__gte=value)
```
- lt: Less than.
```python
ModelName.objects.filter(field__lt=value)
```
- lte: Less than or equal to.
```python
ModelName.objects.filter(field__lte=value)
```
- startswith: Checks if the field starts with the specified value.
```python
ModelName.objects.filter(field__startswith=value)
```
- istartswith: Case-insensitive startswith check.
```python
ModelName.objects.filter(field__istartswith=value)
```
- endswith: Checks if the field ends with the specified value.
```python
ModelName.objects.filter(field__endswith=value)
```
- iendswith: Case-insensitive endswith check.
```python
ModelName.objects.filter(field__iendswith=value)
```
- range: Checks if the field's value is within a specified range.
```python
ModelName.objects.filter(field__range=(start_value, end_value))
```
- isnull: Checks if the field is null.
```python
ModelName.objects.filter(field__isnull=True)  # or False
```

- date: Filters by date.
```python
ModelName.objects.filter(field__date=date_value)
```
- year: Filters by year.
```python
ModelName.objects.filter(field__year=year_value)
ModelName.objects.filter(field__year__gt=year_value)  # greater than
```
- month: Filters by month.
```python
ModelName.objects.filter(field__month=month_value)
```

# Aggregate Functions


- Avg: Calculates the average of a field.
```python
from django.db.models import Avg

data = ModelName.objects.all()
average = data.aggregate(Avg('field'))
```
- Count: Counts the number of objects.
```python
from django.db.models import Count
data = ModelName.objects.all()
count = data.aggregate(Count('field'))
```
- Max: Finds the maximum value of a field.
```python
from django.db.models import Max
data = ModelName.objects.all()
max_value = data.aggregate(Max('field'))
```
- Min: Finds the minimum value of a field.
```python
from django.db.models import Min
data = ModelName.objects.all()
min_value = data.aggregate(Min('field'))
```
- Sum: Calculates the sum of a field.
```python
from django.db.models import Sum
data = ModelName.objects.all()
total = data.aggregate(Sum('field'))
```

# Q Objects
```python
from django.db.models import Q

students = Student.objects.filter(
    Q(name__icontains='john') | Q(age__gte=18)
)
```
> This will return all students whose name contains 'john' or whose age is greater than or equal to 18.
> You can also use `&` for AND operations and `~` for NOT operations:
```python
students = Student.objects.filter(
    Q(name__icontains='john') & ~Q(age__lt=18)
)
```
> This will return all students whose name contains 'john' and whose age is not less than 18.
```python
from django.db.models import Q
students = Student.objects.filter(
    ~Q(id__in=[1, 2, 3]) & Q(name__icontains='john')
)
```
> This will return all students whose name contains 'john' and whose id is not in the list [1, 2, 3].


