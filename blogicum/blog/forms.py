from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment


User = get_user_model()


class CreateOrEditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'is_published',
            'author',
        )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
