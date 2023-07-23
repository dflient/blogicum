from django import forms
from django.contrib.auth import get_user_model

from .models import Category, Comment, Location, Post

User = get_user_model()


class CreateOrEditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
            'comment_count'
        )
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(CreateOrEditPostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            is_published=True)
        self.fields['location'].queryset = Location.objects.filter(
            is_published=True)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
