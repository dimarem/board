from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Ad, Author, Category


class AdTinymce(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Ad, AdTinymce)
admin.site.register(Author)
admin.site.register(Category)
