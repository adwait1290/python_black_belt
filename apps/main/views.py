from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.urls import reverse

from .models import Task, TaskManager
from ..login.models import User, UserManager
import datetime

# Create your views here.
def index(request):
    try:
	cookie = request.session['user_id']
        user =  User.Usermgr.filter(id=request.session['user_id'])
        name = user[0].first_name
        todays_tasks = Task.taskMgr.todays_tasks(user[0].id)
        future_tasks = Task.taskMgr.future_tasks(user[0].id) 

        context = {
            'name': name,
            'todays_tasks': todays_tasks,
            'future_tasks': future_tasks,
            'date' : datetime.date.today()
        }
        return render(request, 'main/home.html', context)
    except KeyError:
        return redirect('/')


def add(request):
    now= datetime.datetime.now()
    user_list =  User.Usermgr.filter(id=request.session['user_id'])
    t_date = request.POST['date']
    t_time = request.POST['time']
    title = request.POST['title']
    t_date_time = ('%s %s' % (t_date, t_time))
    try: 
        t_date_time = datetime.datetime.strptime(t_date_time, '%Y-%m-%d %H:%M')
	print t_date_time
	print now
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Please enter a date in the format YYYY-MM-DD')
        return redirect('../home')

    if len(t_date) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Date Field!')
    elif len(t_date) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Time Field!')
    elif datetime.datetime.now() > t_date_time:
        messages.add_message(request, messages.ERROR, 'Only current and future time is allowed! ')
    elif len(title) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Task Field!')
    
    else:
        task = Task(title=title, date=t_date, time=t_time, creator=user_list[0])
        task.save()
    return redirect(('../home'))


def edit(request, task_id):
    try:
        cookie= request.session['user_id']
        task =  Task.objects.get(id=task_id)
        context = {'task' : task, 'date':task.date.strftime('%Y-%m-%d'), 'time':task.time.strftime('%I:%M %p')}
        return render(request, 'main/edit.html', context)
    except:
	return redirect('/')

def update(request, task_id):

    if request.method == "POST":
        user_list =  User.Usermgr.filter(id=request.session['user_id'])
        task_list =  Task.taskMgr.filter(id=request.POST['id'])
        task = task_list[0]
        context = {'task' : task, 'date':task.date.strftime('%Y-%m-%d')}
        t_date = request.POST['date']
        t_time = request.POST['time']
        title = request.POST['title']
        status = request.POST['status']
        t_date_time = ('%s %s' % (t_date, t_time))
	try:
	    t_date_time = datetime.datetime.strptime(t_date_time, '%Y-%m-%d %H:%M')
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Please enter a date in the format YYYY-MM-DD')
            return redirect('../home')

        if len(t_date) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Date Field!')
            return render(request, 'main/edit.html', context)
        elif len(t_time) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Time Field!')
            return render(request, 'main/edit.html', context)
        elif datetime.datetime.now() > t_date_time:
            messages.add_message(request, messages.ERROR, 'Only current and future time is allowed! ')
            return render(request, 'main/edit.html', context)
        elif len(title) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Task Field!')
            return render(request, 'main/edit.html', context)
        else:
            task_list.update(title=title, date=t_date, time=t_time, status=status, creator=user_list[0])
            #task.save()
            return redirect('../../../home')

def delete(request, task_id):
    task = Task.objects.get(id = task_id)
    task.delete()
    return redirect('../../home')
