from django import forms
from tinymce.widgets import TinyMCE

from .models import Ad


class UploadFileForm(forms.Form):
    """Форма для обработки загрузки файла с помощью плагина TinyMCE"""
    file = forms.FileField()


class AdForm(forms.ModelForm):
    """Форма для создания объявления"""

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Ad
        fields = ['category', 'title', 'preview', 'content']
        widgets = {'content': TinyMCE()}
