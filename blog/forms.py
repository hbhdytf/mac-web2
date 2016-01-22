__author__ = 'pc'
# -*- coding:utf-8 -*-
from django.forms import ModelForm
from blog.models import Tmeta
from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput

obj_seclevel = (
    ('', '-----'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class MetaForm(ModelForm):
    object_name = forms.CharField(label='媒资名', required=True, widget=BootstrapTextInput)
    obj_seclevel = forms.ChoiceField(label="安全级别", required=True, choices=obj_seclevel)
    path = forms.FileField(label='路径', required=True)
    parent_secl_id = forms.CharField(label='分类编号', required=True)

    class Meta:
        model = Tmeta
        fields = ('object_name', 'parent_secl_id', 'obj_seclevel', 'path')
