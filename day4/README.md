# Register class in Admin Panel
- Already did yesterday
# Customize model's look on admin panel

```python
from django.contrib import admin
from .models import Profile, Result
# Register your models here.
admin.site.register(Result)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'roll', 'email', 'city')
    search_fields = ('name', 'roll')
    list_filter = ('city',)

admin.site.register(Profile, ProfileAdmin)
```

# Form

```python
from django import forms
from .models import Profile, Result

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    roll = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=100, required=True)

    def save(self):
        profile = Profile(
            name=self.cleaned_data['name'],
            roll=self.cleaned_data['roll'],
            email=self.cleaned_data['email'],
            city=self.cleaned_data['city']
        )
        profile.save()
        return profile
```
we can also show them as 
    - `{{form.as_ul}}` for ul
    - `{{form.as_table}}` for table
    - `{{form.as_p}}` for in p
    - `{{form.<tag name>}}` for for specified input
  

# Custom form(Mannual One)
 Have done it before

# Form fields Types
![alt text](image.png)

# Built in validators
- ```python
    from django import forms
    from django.core import validators
    def check(value):
        if value[0]!='s':
            raise forms.ValidationError('Name should start with "s"')
    class Registration (forms.Form):
        name = forms.CharField(validators=[validators.
        MaxLengthValidator (10), validators.MinLength Validator()])
        email = forms. EmailField(validators =[check])
        password = forms.CharField(widget=forms.Password Input)
  ```
- 