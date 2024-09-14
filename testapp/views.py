from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from testapp.form import signupform, blogform
from testapp.models import blog


def home(request):
    return render(request, 'testapp/home.html')
@login_required
def loginhome(request):
    blog_list = blog.objects.all().order_by('-created_at')
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    uname = request.user.username
    return render(request, 'testapp/loginhome.html', {'page_obj': page_obj, 'uname': uname})
def signup(request):
    if request.method=='GET':
        form_list=signupform()
        return render(request,'testapp/signup.html',{'form_list':form_list})
    elif request.method=='POST':
        form_capture=signupform(request.POST)
        if form_capture.is_valid():
            # Access cleaned data
            fname = form_capture.cleaned_data['first_name']
            lname = form_capture.cleaned_data['last_name']
            name=fname+' '+lname
            uname = form_capture.cleaned_data['username']
            user=form_capture.save()
            user.set_password(user.password)
            user.save()
            return render(request,'testapp/registered.html',{'name':name,'uname':uname})
@login_required
def logouts(request):
    logout(request)
    return redirect('logout_redirect')
def logout_redirect(request):
    return render(request,'testapp/logout.html')
@login_required
def create(request):
    if request.method == 'POST':
        form = blogform(request.POST)
        if form.is_valid():
            if form.is_valid():
                blog_instance = form.save(commit=False)  # Create a blog instance but don’t save it to the database yet
                blog_instance.user = request.user  # Assign the current user to the blog instance
                blog_instance.save()
            return render(request,'testapp/myblog.html',{'blog':blog_instance})  # Redirect to a page listing all blogs or any other page
    else:
        form = blogform()

    return render(request, 'testapp/create_blog.html', {'form': form})
@login_required
def profile(request,uname):
    blogs=blog.objects.filter(user=uname).order_by('-created_at')
    if blogs:
        return render(request, 'testapp/profile.html', {'blogs': blogs})
