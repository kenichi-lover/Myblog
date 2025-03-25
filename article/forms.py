from django import forms
from .models import ArticleInfo,ArticleTag

class ArticleForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=ArticleTag.objects.all(),
                                         widget=forms.CheckboxSelectMultiple,
                                         required=False)
    class Meta:
        model = ArticleInfo
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }