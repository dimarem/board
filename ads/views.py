from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ad, Author
from .forms import UploadFileForm, AdForm


class AdsList(ListView):
    """Список объявлений"""
    model = Ad
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(DetailView):
    """Детальное описание объявления"""
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


class AdCreate(LoginRequiredMixin, CreateView):
    """Создать объявление"""
    model = Ad
    template_name = 'ad_edit.html'
    form_class = AdForm

    def form_valid(self, form):
        ad = form.save(commit=False)
        author = Author.objects.filter(user=self.request.user).first()

        if not author:
            author = Author.objects.create(user=self.request.user)

        ad.author = author

        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    """Изменить объявление"""
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'


def upload_file(request):
    """Обработчик загрузки файло с помощью TinyMCE"""
    form = UploadFileForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseBadRequest()

    file = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    return HttpResponse(uploaded_file_url)
