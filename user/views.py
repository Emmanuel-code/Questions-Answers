from django.contrib.auth import authenticate,login

from .forms import SignUpForm,UpdateProfileForm
from .models import Profile
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def edit_profile(request):
    if request.method=='POST':
        form=UpdateProfileForm(request.POST, files=request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form=UpdateProfileForm(instance=request.user)
    return render(request, 'user/edit.html',{'form':form})




def register(request):
    form=SignUpForm(request.POST)
    if form.is_valid():
        user=form.save()
        user.refresh_from_db()
        user.first_name=form.cleaned_data.get('first_name')
        user.last_name=form.cleaned_data.get('last_name')
        user.email=form.cleaned_data.get('email')
        user.save()
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password1')
        user=authenticate(username=username,password=password)
        login(request,user)
        return redirect('user:login')
    else:
        form=SignUpForm()
    return render(request,'user/register.html',{'form':form})


@login_required
def profile(request):
    prof=Profile.objects.get(user=request.user)
    return render(request, 'user/profile.html', {'prof':prof})

def about(request):
    return render(request,'user/about.html',{})


@login_required
def public_profile(request):

    return render(request, 'user/public_profile.html', {})
