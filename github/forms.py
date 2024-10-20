from django import forms

class GitHubLinkForm(forms.Form):
    github_username = forms.CharField(max_length=150, required=True)
