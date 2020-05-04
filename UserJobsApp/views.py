from django.shortcuts import render , HttpResponse , redirect
from .models import Users , Jobs , User_Category
from django.contrib import messages
import bcrypt
# Create your views here.


def index(request):
    return render(request,'index.html')


def register(request):
    errors = Users.objects.basic_validator(request.POST)
    hashPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        logged_user = Users.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashPW
        )
        User_Category.objects.create(category = 'Pet Care' , User = logged_user)
        User_Category.objects.create(category = 'Electrical' , User = logged_user)
        User_Category.objects.create(category = 'Garden' , User = logged_user)
        request.session['userID'] = logged_user.id
        return redirect('/dashboard')

def login(request):
    user = Users.objects.filter(email=request.POST['email']) 
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userID'] = logged_user.id
            return redirect('/dashboard')
    messages.error(request,'Invalid email or password')
    return redirect("/")

def dashboard(request):
    if request.session.get('userID', None) == None:
        return redirect("/")
    user = Users.objects.get(id = int(request.session['userID']))
    all_jobs = Jobs.objects.exclude(assigned_to = user)
    context = {
        'User' : user,
        'all_jobs' : all_jobs
    }
    return render(request,'dashboard.html',context)

def new_job(request):

    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_user = Users.objects.get(id = request.session['userID'])
    context = {
        'Categories' : cur_user.Category.all()
    }
    return render(request,'new_job.html',context)

def create_job(request):
    if request.session.get('userID', None) == None:
        return redirect("/")
    
    errors = Jobs.objects.basic_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/Jobs/New')
    else:



        cur_user = Users.objects.get(id = int(request.session['userID']))
        cur_job = Jobs.objects.create(title = request.POST['title'],
            desc = request.POST['desc'],
            location = request.POST['location'],
            created_by = cur_user,
            assigned_to = cur_user
        )
        for index,var in request.POST.items():
            if str(index).isdigit() and var == 'True':
                cur_job.category.add(User_Category.objects.get(id = index))
        if request.POST['other'] != None:
            UC = User_Category.objects.create(category = request.POST['other'],User = cur_user)
            cur_job.category.add(UC)
        
        return redirect('/dashboard')

def edit_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")

    user = Users.objects.get(id = int(request.session['userID']))
    cur_job = Jobs.objects.get(id = Job_ID)
    
    context = {
        'User' : user,
        'Job' : cur_job
    }
    return render(request,'edit_job.html',context)

def view_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    user = Users.objects.get(id = int(request.session['userID']))
    cur_job = Jobs.objects.get(id = Job_ID)
    categories = cur_job.category.all()
    for var in categories:
        print(var.category)
    print(categories)
    context = {
        'User' : user,
        'Job' : cur_job,
        'categories' : categories
    }
    return render(request,'view_job.html',context)

def update_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    errors = Jobs.objects.basic_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/Jobs/Edit/{Job_ID}')
    else:
        cur_job = Jobs.objects.get(id = Job_ID)
        cur_job.title = request.POST['title']
        cur_job.desc = request.POST['desc']
        cur_job.location = request.POST['location']
        cur_job.save()
        return redirect('/dashboard')


def assign_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_job = Jobs.objects.get(id = Job_ID)
    cur_job.assigned_to = Users.objects.get(id = int(request.session['userID']))
    cur_job.save()
    return redirect('/dashboard')

def unassign_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_job = Jobs.objects.get(id = Job_ID)
    cur_job.assigned_to = None
    cur_job.save()

    return redirect('/dashboard')

def remove_job(request,Job_ID):
    if request.session.get('userID', None) == None:
        return redirect("/")
    cur_job = Jobs.objects.get(id = Job_ID)
    cur_job.delete()
    return redirect('/dashboard')


def log_out(request):
    request.session.flush()
    return redirect('/')
