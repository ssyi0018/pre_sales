# 定义样式类，继承modelform
from django import forms


# 写一个公共类，下面两个类共同继承，并分别继承ModelForm和Form
class BootStrap:
    # 定义列表移除bootstrap样式
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs['class'] = "form-control"
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': "form-control",
                                      'placeholder': field.label}


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
