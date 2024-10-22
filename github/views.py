import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GitHubLinkForm

@login_required
def link_github(request):
    if request.method == 'POST':
        form = GitHubLinkForm(request.POST)
        if form.is_valid():
            # Save the GitHub username or token in the user profile
            github_username = form.cleaned_data['github_username']
            # Save to user profile or another model (implement logic)
            return redirect('github_projects')
    else:
        form = GitHubLinkForm()
    return render(request, 'github/link.html', {'form': form})

@login_required
def fetch_github_projects(request):
    # Get the GitHub username from the user profile
    github_username = request.user.profile.github_username  # example profile field

    # Fetch projects from GitHub API
    url = f'https://api.github.com/users/{github_username}/repos'
    response = requests.get(url)
    projects = response.json()

    # Pass the projects to the template
    return render(request, 'github/projects.html', {'projects': projects})

@login_required
def add_project_to_resume(request, project_id):
    # Logic to add the GitHub project to the resume
    # Fetch the project details from the GitHub API and add it to the resume
    return redirect('resume_detail', id=request.user.resume.id)
