from django import forms
from .models import AlbumInfo

class AlbumInfoForm(forms.ModelForm):
    class Meta:
        model = AlbumInfo
        fields = ['title', 'introduce', 'photo']  # 指定要包含的字段
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'introduce': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '标题',
            'introduce': '描述',
            'photo': '图片',
        }