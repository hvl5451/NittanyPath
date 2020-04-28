from django import forms
from .models import Posts, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('post_info', )


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('comment_info', )
