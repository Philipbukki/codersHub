from django import forms
from .models import Project
from django.forms import widgets


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['featured_image', 'title', 'description',
                  'source_link', 'demo_link', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        widgets

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
          #  {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})
