from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from .forms import NotesForm, HomeworkForm, DashboardForm, TodoForm, UserRegistrationForm
from .models import Notes, Homework, Todo

# Home page
def home(request):
    return render(request, 'dashboard/home.html')

# Notes list and creation
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Note added successfully by {request.user.username}!")
            return redirect('notes')
    else:
        form = NotesForm()

    notes_list = Notes.objects.filter(user=request.user)
    context = {'notes': notes_list, 'form': form}
    return render(request, 'dashboard/notes.html', context)

# Delete note
def delete_note(request, pk=None):
    Notes.objects.filter(id=pk, user=request.user).delete()
    return redirect("notes")

# Note detail view
class NotesDetailView(generic.DetailView):
    model = Notes
    context_object_name = 'note'
    template_name = 'dashboard/note_detail.html'

# Homework page
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished') == 'on'
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(request, f'Homework added by {request.user.username}!')
            return redirect('homework')
    else:
        form = HomeworkForm()

    homework_list = Homework.objects.filter(user=request.user)
    homework_done = not homework_list.exists()

    context = {
        'homework': homework_list,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

# Update homework completion status
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')

# Delete homework
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

# YouTube search view
def youtube(request):
    form = DashboardForm()
    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)

# Todo view with form handling
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo')
    else:
        form = TodoForm()
    todo_list = Todo.objects.filter(user=request.user)
    context = {'form': form, 'todos': todo_list}
    return render(request, "dashboard/todo.html", context)

# Books view
def books(request):
    form = DashboardForm()
    context = {'form': form}
    return render(request, "dashboard/books.html", context)

def dictionary(request):
    return render(request, "dashboard/dictionary.html")

def wiki(request):
    return render(request, "dashboard/wiki.html")

def conversion(request):
    return render(request, "dashboard/conversion.html")

# Register view (fixed RegisterForm issue)
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, "Account created for {{usename}}!!")
            return  redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request, "dashboard/register.html", context)


def profile(request):
    return render (request,"dashboard/profile.html")