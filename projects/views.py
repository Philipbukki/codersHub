from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from django.shortcuts import render, redirect
from. models import Project, Tag


@login_required(login_url="login")
def projects(request):
    projects = Project.objects.all()
    tags = Tag.objects.all()
    context = {
        'projects': projects,
        'tags': tags
    }
    return render(request, 'projects/projects_list.html', context)


@login_required(login_url="login")
def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    context = {
        'project': project,
        'tags': tags
    }
    return render(request, 'projects/project_detail.html', context)


@login_required(login_url="login")
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('projects')

    else:
        form = ProjectForm()

    context = {
        'form': form,
    }
    return render(request, 'projects/add.html', context)


@login_required(login_url="login")
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()

            return redirect('projects')

    context = {
        'form': form,
    }
    return render(request, 'projects/add.html', context)


@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {
        'object': project,
    }
    return render(request, 'projects/delete_project.html', context)
