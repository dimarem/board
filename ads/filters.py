from django_filters import FilterSet, CharFilter, BooleanFilter
from django_filters.widgets import BooleanWidget
from django.forms import TextInput

from .models import Feedback


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("unknown", "Все"), ("true", "Да"), ("false", "Нет"))
        self.attrs = {'class': 'form-control'}


class FeedbackFilter(FilterSet):
    content = CharFilter(field_name='content', lookup_expr='icontains',
                         widget=TextInput(attrs={'class': 'form-control'}), label='Отзыв содержит')

    ad = CharFilter(field_name='ad__content', lookup_expr='icontains',
                    widget=TextInput(attrs={'class': 'form-control'}), label='Объявление содержит')

    author = CharFilter(field_name='author__username', lookup_expr='icontains',
                        widget=TextInput(attrs={'class': 'form-control'}), label='Автор')

    # accepted = BooleanFilter(field_name='accepted', label='Принят')
    accepted = BooleanFilter(field_name='accepted', label='Принят', widget=CustomBooleanWidget())

    class Meta:
        model = Feedback
        fields = []
