from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Todo
from django.utils import timezone
from .forms import TodoForm, CreateUserForm
from email.message import EmailMessage
import smtplib

# Import Settings file
from django.conf import settings as conf_settings


def sendmail(to_message, subject='', message=''):
    if conf_settings.EMAIL_HOST_USER == "":
        return
    msg = EmailMessage()
    msg['From'] = conf_settings.EMAIL_HOST_USER
    msg['To'] = to_message
    msg['Subject'] = subject
    msg.set_content(message)
    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(conf_settings.EMAIL_HOST_USER, conf_settings.EMAIL_HOST_PASSWORD)
    server.send_message(msg)
    server.quit()


def signupuser(request):
    if request.user.is_authenticated:
        return redirect('currenttodos')

    if request.method == 'GET':
        return render(request, 'notes/signupuser.html', {'form': CreateUserForm()})
    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'],
                                                first_name=request.POST['first_name'], email=request.POST['email'])
                user.save()
                login(request, user)
                # send on-register email
                sub = 'Thank you for registering'
                msg = 'Dear ' + request.user.username + ',\nWelcome to Schedule.It.\nWe are glad to have you aboard. Keep crushing and updating tasks at scheduleIT.pythonanywhere.com.'
                sendmail(request.user.email, sub, msg)
                return redirect('currenttodos')
            except IntegrityError:

                return render(request, 'notes/signupuser.html', {'form': CreateUserForm(),
                                                                 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'notes/signupuser.html',
                          {'form': CreateUserForm(), 'error': 'Passwords did not match. Please try again'})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('currenttodos')

    if request.method == 'GET':
        return render(request, 'notes/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'notes/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True).count()
            if todos > 5:
                # send reminder mail
                sub = str(todos) + ' To-dos left to complete !'
                msg = 'Dear ' + request.user.username + '\nYou have ' + str(todos) + ' remaining to-dos.\nMake sure to finish them and reach your goals!!\n\nKeep crushing and updating tasks at scheduleIT.pythonanywhere.com.'
                sendmail(request.user.email, sub, msg)
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')
    else:
        return redirect('currenttodos')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'notes/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True).count()
            mail = 0
            if todos > 5:
                # send reminder mail
                sub = str(todos) + ' To-dos left to complete !'
                msg = 'Dear ' + request.user.username + ',\nYou have ' + str(todos) + ' remaining to-dos.\nYou just added ' + newtodo.title + '\nMake sure to finish them and reach your goals!!\n\nKeep crushing and updating tasks at scheduleIT.pythonanywhere.com.'
                sendmail(request.user.email, sub, msg)
                mail = 1
            if newtodo.important and mail == 0:
                # send important to-do note mail
                sub = 'You added an important note on Schedule.It'
                msg = 'Dear ' + request.user.username + ',\nYou have added an important note. ' + newtodo.title + '\nCrush the task and visit us back!'
                sendmail(request.user.email, sub, msg)
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'notes/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'notes/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'notes/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'notes/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            newtodo = form.save(commit=False)
            if newtodo.important:
                # send important to-do updation email
                sub = 'You updated an important note on Schedule.It'
                msg = 'Dear ' + request.user.username + ' you have updated an important note. ' + newtodo.title + '\nCrush the task and visit us back!\n\nKeep crushing and updating tasks at scheduleIT.pythonanywhere.com.'
                sendmail(request.user.email, sub, msg)
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
