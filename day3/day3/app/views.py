from django.shortcuts import render
from .models import Student
# Create your views here.
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'student_detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        student = Student(name=name, age=age, email=email)
        student.save()
        return render(request, 'student_detail.html', {'student': student})
    return render(request, 'student_create.html')

def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.age = request.POST.get('age')
        student.email = request.POST.get('email')
        student.save()
        return render(request, 'student_detail.html', {'student': student})
    return render(request, 'student_update.html', {'student': student})

def student_delete(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.delete()
        return render(request, 'student_list.html', {'students': Student.objects.all()})
    return render(request, 'student_delete.html', {'student': student})