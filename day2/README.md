# How to run Django Project on a specific port:-
<u>Default</u>
```cmd
python manage.py runserver
```

<u>To run it on a specific port:-</u>
```cmd
python manage.py runserver <port number>
```

---

# How to create django Applications
```cmd
django-admin startapp <appname>
```

## why do we even need applications in django?

1. Separation of Concerns
2. Reusability
3. Better Testing
4. Team collaboration
5. Pluggability

---

# Function Based View

- write functions in view.py
- add them in urls.py with the urls using path
- if we are creating multiple apps we have to use them with `as`

---
# URL PATTERN
- path function -> It needs url,view function, kwargs, name
- Best option ->
  - set urls.py in the separate apps and combine them in the project's url file


# Templates
- Django works on mvt(Model -> View -> Template) architecture
- we use render for it
- Best practice is to have them separately in each application

---

# Dynamic template
- here we can use jinja templates
- we have to sent a context (a dictionary)

---

# Django Template language

``` DTL is the default templating engine in Django.
 It's simple yet powerful, allowing HTML + Python-like logic inside templates.
 Alternatives like Jinja2 can be used, but require additional configuration.
```
- Basic Setup:
  - Django project and app creation (`startproject`, `startapp`).
  - Register the app in `INSTALLED_APPS` in `settings.py`.
  - Create a `templates` directory inside the app folder.
  - Structure: `app/templates/app_name/template.html`.

- Using Views with Templates:
  - Views use `render(request, template_name, context)` to pass data to templates.
  - Context is a dictionary of variables passed to the template.

- Variable Display in Templates:
  - Syntax: `{{ variable_name }}` to display variables.
  - You can pass complex dictionaries and access nested data.

- Filters in Templates:
  - Filters modify variable output. Examples:
    - `{{ name|lower }}` → lowercase
    - `{{ name|upper }}` → uppercase
    - `{{ name|truncatewords:3 }}` → limit to 3 words
    - `{{ name|length }}` → shows character count
    - `{{ name|default:"Guest" }}` → default value if variable is empty

- Date & Time Formatting:
  - Use `{{ date_var|date:"D d M Y" }}` for custom formats
  - Use `{{ time_var|time:"H:i" }}` for time
  - Built-in filters like `short_date_format` and `short_time_format` available.

- Float Formatting (Monetary/Precision Control):
  - Use `{{ price|floatformat:2 }}` to round to 2 decimal places
  - Supports positive, zero, and negative precision

- Conditionals: if, if-else, if-elif-else:
  - {% if variable %}...{% endif %}
  - {% if var == 'value' %}...{% else %}...{% endif %}
  - Support for and, or, not, and comparisons (==, !=, <, >)

# Template Inheritance
- Here we use it to redduce code redundancy
- to use tratic files we have to add {% load static %} 