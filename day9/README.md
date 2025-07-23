# Fix CSS static files

In `runserver` the static files are served. But in case of `daphne` and `uvicorn` the static files are not served by default.

## 1 (Development)

```python
# asgi.py
...
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

application = ASGIStaticFilesHandler(
    get_asgi_application()
)
```

## 2 (Production)

```python
# settings.py
...
STATIC_ROOT = BASE_DIR / "static"

```

```python
# urls.py
...
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
...
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

```bash
# collect static files
python manage.py collectstatic
```

# Django Async ORM

![alt text](image.png)

![alt text](image-1.png)

Asynchronous ORM for Django, which allows you to use Django's ORM in an asynchronous context. It is built on top of Django's ORM and provides a simple and easy-to-use interface for working with databases in an asynchronous way.
The available methods are:

- `acount()`: Returns the number of objects matching the query.
- `aget()`: Returns a single object matching the query.
- `afirst()`: Returns the first object matching the query.
- `alast()`: Returns the last object matching the query.
- `aexists()`: Returns True if the query has any results, False otherwise.
- `aget_or_create()`: Returns a single object matching the query, or creates it if it does not exist.
- `aget_or_none()`: Returns a single object matching the query, or None if it does not exist.
- `alatest()`: Returns the last object matching the query.
- `aearliest()`: Returns the first object matching the query.
- `aexplains()`: Returns a list of objects matching the query.
- `aiterate()`: Returns an asynchronous iterator over the objects matching the query.
- `aprefetch_related()`: Prefetches related objects for the query.
- `abulk_create()`: Creates multiple objects in bulk.
- `abulk_update()`: Updates multiple objects in bulk.
- `abulk_delete()`: Deletes multiple objects in bulk.
- `aupdate()`: Updates the objects matching the query.
- `adelete()`: Deletes the objects matching the query.

```python
# Example
from django.http import JsonResponse
from myapp.models import MyModel

async def home(request):
    result = MyModel.objects.all()
    async for obj in result:
        print(obj)
    await MyModel.objects.acreate(name="New Object", value=42)
    data = [{"id": obj.id, "name": obj.name, "value": obj.value} for obj in result]
    hello = await MyModel.objects.aget(pk=1)
    await hello.adelete()

    return JsonResponse(data, safe=False)
```

# Async Django Middleware

In django, middleware is a way to process requests globally before they reach the view or after the view has processed them.
now by default, middleware is synchronous, but you can create asynchronous middleware by using decorators.

## functional decorators

```python
# Example
from django.http import JsonResponse
from django.utils.decorators import sync_and_async_middleware,sync_only_middleware,async_only_middleware

@sync_only_middleware
def my_sync_middleware(get_response):
    def middleware(request):
        # Do something before the view is called
        response = get_response(request)
        # Do something after the view is called
        return response

    return middleware

@async_only_middleware
async def my_async_middleware(get_response):
    async def middleware(request):
        # Do something before the view is called
        response = await get_response(request)
        # Do something after the view is called
        return response

    return middleware


@sync_and_async_middleware
async def my_middleware(get_response):
    async def middleware(request):
        if iscoroutinefunction(get_response):
            # If get_response is an async function
            response = await get_response(request)
        else:
            # If get_response is a sync function
            response = get_response(request)
        return response

    return middleware
```

now sync_and_async_middleware is a decorator that allows you to create middleware that can handle both synchronous and asynchronous requests. it checks the type using `iscoroutinefunction` and calls the appropriate function accordingly.
It is said that one should not use sync_and_async_middleware in production, as it can lead to performance issues. Instead, you should use either sync_only_middleware or async_only_middleware depending on your use case.

## Class-based middleware

```python
from asyncio import iscoroutinefunction
from django.utils.asyncio import markcoroutinefunction

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Adapt self.async_capable based on the type of get_response
        if iscoroutinefunction(get_response):
            # If get_response is an async function, mark this middleware as async
            markcoroutinefunction(self)
            self.async_capable = True
            self.sync_capable = False
        else:
            # If get_response is a sync function, this middleware is sync
            self.async_capable = False
            self.sync_capable = True

    async def __call__(self, request):
        # Logic before the view is called
        response = await self.get_response(request)
        # Logic after the view is called
        return response
```


# Class-based views
class-based views in Django are a way to organize your views in a more structured way. They allow you to define your views as classes, which can make your code more reusable and easier to maintain.

# Example
```python
# views.py
from django.views import View
from django.http import JsonResponse

class MyView(View):
    def get(self, request):
        data = {"message": "Hello, world!"}
        return JsonResponse(data)
    def post(self, request):
        data = {"message": "Hello, world!"}
        return JsonResponse(data, status=201)
```
```python
# urls.py
from django.urls import path
from .views import MyView

urlpatterns = [
    path('my-view/', MyView.as_view(), name='my_view'),
]
```

to access the views like /my-view/<id:int> you can use the `get` method in the class-based view.
```python
# views.py
from django.views import View
from django.http import JsonResponse
from myapp.models import MyModel

class MyView(View):
    def get(self, request, id):
        obj = MyModel.objects.get(pk=id)
        data = {"message": obj.name}
        return JsonResponse(data)
```
```python
# urls.py
from django.urls import path
from .views import MyView

urlpatterns = [
    path('my-view/<int:id>/', MyView.as_view(), name='my_view'),
]
```


```python
class MyView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        return JsonResponse({
            "status": "success",
            "message": f"Class view accessed with id: {id}"
        })
    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        return JsonResponse({
            "status": "success",
            "message": "Post request received",
            "data": {"id": id}
        })
```

# Tewmplate Views
Template views are a way to render templates in Django using class-based views. They provide a simple way to render templates without having to write a lot of boilerplate code.
```python
# urls.py
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('template-view/', TemplateView.as_view(template_name='myapp/template.html'), name='template_view'),
]
```

We can also do it using views.py
```python
# views.py
from django.views.generic import TemplateView

class MyTemplateView(TemplateView):
    template_name = 'myapp/template.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Hello, world!'
        return context
```

# Redirect Views
Redirect views are a way to redirect users to a different URL in Django using class-based views.
```python
# urls.py
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('redirect-view/', RedirectView.as_view(url='/new-url/'), name='redirect_view'),
    path('new-url/', TemplateView.as_view(template_name='myapp/template.html'), name='new_url'),
    path('old-url/', RedirectView.as_view(pattern_name='new_url'), name='old_url'),
]
```
```python
# views.py
from django.views.generic import RedirectView

class MyRedirectView(RedirectView):
    url = '/new-url/'
    permanent = False  # Set to True for a permanent redirect (HTTP 301)
```

# Generic class-based views
Generic class-based views are a way to create views that handle common tasks in Django, such as displaying a list of objects, creating a new object, updating an existing object, or deleting an object.
Django provides several built-in generic class-based views that you can use to quickly create these views.

## Display Views

- ### ListView:-
    The ListView is used to display a list of objects from a model. It inherits from the `MultipleObjectMixin`,`templateresponsemixin` and `baseview`, `MultipleObjectMixin`,`View` classes.` and provides pagination support.

    ```python
    # views.py
    from django.views.generic.list import ListView
    from myapp.models import MyModel

    class MyListView(ListView):
        model = MyModel
    ```
    >Default template name for ListView is `<model_name>_list.html`. For example, if your model is `MyModel`, the default template will be `mymodel_list.html`. Also the context variable will be `<ModelName>_list` by  default.

    ```python
    # views.py
    from django.views.generic.list import ListView
    from myapp.models import MyModel
    class MyListView(ListView):
        model = MyModel
        template_name_suffix = 'all' # to change the default template name's suffix
        context_object_name = 'my_objects'
        ordering = ['name']
    class MyListView2(ListView):
        model = MyModel
        template_name = 'myapp/my_list.html'
        context_object_name = 'my_objects' # to change the context name
        # to customize the list query 
        def get_queryset(Self):
            return MyModel.objects.filter(name__startswith='A')
        # to add more context
        def get_context_data(self, **args, **kwargs):
            context = super().get_context_data(**args, **kwargs)
            context['message'] = 'Hello, world!'
            return context
     
    ```

- ### DetailView:-
    The DetailView is used to display a single object from a model.
    ```python
    # view.py
    from django.views.generic.detail import DetailView
    from myapp.models import MyModel

    class MyDetailView(DetailView):
        model = MyModel
    ```
    >Default template name for DetailView is `<model_name>_detail.html`. The get field is `pk` by default.
    ```python
    # urls.py
    from .views import MyDetailsView

    urlpatterns =[
        path('object/<int:pk>/', MyDetailView.as_view(), name='my_detail')
    ]
    ```
    to change that:-
    ```python
    from django.views.generic.detail import DetailView
    from myapp.models import MyModel
    class MyDetailView(DetailView):
        model = MyModel
        pk_url_kwarg = 'my_id'
        template_name = 'myapp/my_detail.html'
        context_object_name = 'my_object'
        # template_suffix = '_custom'
        def get_context_data(self,**args,**kwargs):
            context = super().get_context_data(**args,**kwargs)
            context['message'] = 'Hello, world!'
            return context
    ```
- ### FormView:-
    The FormView is used to display a form and handle form submission. It inherits from the `FormMixin` and `BaseView` classes.
    ```python
    # views.py
    from django.views.generic.edit import FormView
    from myapp.forms import MyForm
    from myapp.models import MyModel
    class MyFormView(FormView):
        template_name = 'myapp/my_form.html'
        form_class = MyForm
        success_url = '/success/'  # URL to redirect after successful form submission
        def form_valid(self, form):
            # Logic to handle the form submission
            form_data = form.cleaned_data
            MyModel.objects.create(**form_data)
            # For example, save the form data or send an email
            return super().form_valid(form)
    ```
    >Default template name for FormView is `<form_class_name>_form.html`. For example, if your form class is `MyForm`, the default template will be `myform_form.html`. 
    ```python
    # urls.py
    from .views import MyFormView
    urlpatterns = [
        path('form/', MyFormView.as_view(), name='my_form'),
    ]
    ```
- ### CreateView:-
    The CreateView is used to create a new object in the database. It inherits from the `SingleObjectTemplateMixin`, `TemplateResponseMixin`, and `BaseCreateView` classes.
    ```python
    # views.py
    from django.views.generic.edit import CreateView
    from myapp.models import MyModel
    from myapp.forms import MyForm
    class MyCreateView(CreateView):
        model = MyModel
        fields = ['name', 'value']  # Fields to include in the form
        # form_class = MyForm  # Use a custom form class if needed
        template_name = 'myapp/mymodel_form.html'
        success_url = '/success/'
        def get_absolute_url(self):
            return f"/mymodel/{self.object.pk}/"  # Redirect to the detail view of the created object
        def get_form(self, form_class=None):
            form = super().get_form(form_class)
            # Customize the form if needed
            form.fields['name'].label = 'Custom Name'
            form.widgets['value'].attrs.update({'placeholder': 'Enter value'})
            return form
    ```
    >Default template name for CreateView is `<model_name>_form.html`. For example, if your model is `MyModel`, the default template will be `mymodel_form.html`.
- ### UpdateView:-
    The UpdateView is used to update an existing object in the database. It inherits from the `SingleObjectTemplateMixin`, `TemplateResponseMixin`, and `BaseUpdateView`,`ModelFormMixin`,`FormMixin`,`SingleObjectMixin` classes.
    
    ```python
    # views.py
    from django.views.generic.edit import UpdateView
    from myapp.models import MyModel
    from myapp.forms import MyForm
    class MyUpdateView(UpdateView):
        model = MyModel
        fields = ['name', 'value']  # Fields to include in the form
        # form_class = MyForm  # Use a custom form class if needed
        template_name = 'myapp/mymodel_form.html'
        success_url = '/success/'
        
        def get_object(self, queryset=None):
            return MyModel.objects.get(pk=self.kwargs['pk'])  # Get the object to update
        def get_form(self, form_class=None):
            form = super().get_form(form_class)
            # Customize the form if needed
            form.fields['name'].label = 'Custom Name'
            return form
    ```
- ### DeleteView:- 
    The DeleteView is used to delete an object from the database. It inherits from the `SingleObjectTemplateMixin`, `TemplateResponseMixin`, and `BaseDeleteView`,`SingleObjectMixin` classes.
    ```python
    # views.py
    from django.views.generic.edit import DeleteView
    from myapp.models import MyModel
    from django.urls import reverse_lazy
    class MyDeleteView(DeleteView):
        model = MyModel
        template_name = 'myapp/mymodel_confirm_delete.html'
        success_url = reverse_lazy('my_list')
   