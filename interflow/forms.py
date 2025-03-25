from django import forms
from .models import Board

class InterflowInfoForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'email','content']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            #if name == 'name':
                #continue
            field.widget.attrs = {'class':'form-control','placeholder':field.label,'style':'background-color: transparent'}


'''
如果不设置表单label的颜色，对应的index.html表单直接可以这样：
<form method="post">
    {% csrf_token %}
    
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">提交留言</button>
</form>

'''