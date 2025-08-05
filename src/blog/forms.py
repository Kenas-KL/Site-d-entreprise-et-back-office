from django import forms
from .models import Task, BlogPost, CustomUser, Comment



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'date_de_debut', 'date_de_fin', 'priorite', 'statut', 'avancement', 'commentaires',
        ]
        widgets = {
            'date_de_debut': forms.DateTimeInput(attrs={'type': 'date'}),
            'date_de_fin': forms.DateTimeInput(attrs={'type': 'date'}),
        }


class TaskForm_(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'date_de_fin', 'priorite', 'statut', 'avancement', 'commentaires',
        ]
        widgets = {
            'date_de_fin': forms.DateTimeInput(attrs={'type': 'date'}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title", "content", "published",
        ]


class FormulaireInscription(forms.ModelForm):
    Mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    Confirmation_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            "username",
        )

    def clean(self):
        cleaned_data= super().clean()
        Mot_de_passe = cleaned_data.get('Mot_de_passe')
        Confirmation_mot_de_passe = cleaned_data.get('Confirmation_mot_de_passe')

        if Mot_de_passe != Confirmation_mot_de_passe:
            raise forms.ValidationError("les mots de passe ne correspondent pas.")
        return cleaned_data


class FormComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
