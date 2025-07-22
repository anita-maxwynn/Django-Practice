# How to add bootstrap
1. Using CDN link
2. Using pip library  
   > Then you have to declare it in the `settings.py` as an installed app and in the `base.html` as `{% load django_bootstrap5 %}`

# How to use Tailwind CSS
~~We have to use node
There's also a pip library which we can use
Then we have to init it as an app
and declare it in settings.py~~ [old process]

1. First, set up a new folder.
2. Then run:
   ```bash
   npm install tailwindcss @tailwindcss/cli
   ```
3. Inside that folder, create a new CSS file and add:
   ```css
   @import "tailwindcss";
   ```
4. Finally, run:
   ```bash
   npx tailwindcss -i ./src/input.css -o ./src/output.css --watch
   ```
5. start using css in your html


# Hyperlink
In url.py we set names to urls. We use them to create hyperlinks in the frontend
The process is to use "{% url '<urlname>' %}" in the href



# ORM(Object Relational Manner)
it provides the interaction between the application and the database!
[alt text](image.png)
In django's orm it let's us write sql quaries in python

# model
A model in Django is a Python class that represents a database table.
It is the single, definitive source of information about your data.
It contains the essential fields and behaviors of the data you're storing.
Models define the structure of stored data, including field types, defaults, options, etc.
Each model maps to a single database table.

# retriving data from models
```python
val = Modelname.objects.all() # to get all
```

```python
val = Modelname.objects.get(seatsching_parameter = "something") # to get filtered
```

# Superuser
```cmd
python manage.py createsuperuser
```
> A Django superuser is a special kind of user account that has full administrative access to all parts of your Django project — especially the Django admin panel.

## Superuser Permissions:
- Can log into the admin panel (/admin/).
- Can view, add, edit, delete any model's data.
- Can create or manage other users (including staff and other superusers).
- Has all permissions by default, without needing to be explicitly assigned.
