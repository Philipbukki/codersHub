from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from. models import Project, Tag


@login_required(login_url="login")
def projects(request):
    projects, search_query = searchProjects(request)
    paginator = Paginator(projects, 2)
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {
        'projects': projects,
        'search_query': search_query,
        'page': page,
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
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            return redirect('projects')

    else:
        form = ProjectForm()

    context = {
        'form': form,
    }
    return render(request, 'projects/add.html', context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
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
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {
        'object': project,
    }
    return render(request, 'projects/delete_project.html', context)
