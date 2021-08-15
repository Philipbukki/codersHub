from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Skill
from .utils import searchProfiles


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created")
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Opps! an error occurred during sign Up")

    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, "Username does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, "username or password is incorrect!")

    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def profile(request):
    profiles, search_query = searchProfiles(request)
    paginator = Paginator(profiles, 1)
    page = request.GET.get('page')

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    context = {
        'profiles': profiles,
        'page': page,
        'search_query': search_query,
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):

    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/user_profile.html', context)


def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }

    return render(request, 'users/account.html', context)


def updateAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form
    }

    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added!")
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {
        'object': skill,
    }
    return render(request, 'users/delete_skill.html', context)
