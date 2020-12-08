# 2015244055 김성민
# DB에서 받은 객체를 페이지에 보여주기 
from django import forms
from .models import Post,SecretBorad

class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        title = forms.CharField(
            widget=forms.Textarea(attrs={'class': 'post_create'}
        )
        )
        content = forms.CharField(widget=forms.Textarea(attrs={'class': 'post_create',
        'rows': 5,
        'cols': 50, }
    )
        )

        labels = {
            'title': '제목',
            'content': '내용',
            'image': '사진',
        }
        required = {
            
            'image':False,
        }

class SecretForm(forms.ModelForm):
    class Meta:
        model = SecretBorad
        fields = ['title','content','image','private']
        title = forms.CharField(
            widget=forms.Textarea(attrs={'class': 'post_create'}
        )
        )
        content = forms.CharField(widget=forms.Textarea(attrs={'class': 'post_create',
        'rows': 5,
        'cols': 50, }
    )
        )
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '사진',
            'private': '비밀글 체크',
        }
        required = {
            'image':False,
            'private':False,
        }
