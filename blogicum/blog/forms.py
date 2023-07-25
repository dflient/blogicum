from django import forms

from .models import Category, Comment, Location, Post


class CreateOrEditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = (
            'author',
            'comment_count'
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%d-%m-%Y %H:%M:%S',
            )
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
