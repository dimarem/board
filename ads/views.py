from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Ad, Author, Feedback
from .forms import UploadFileForm, AdForm
from .filters import FeedbackFilter


class AdsList(ListView):
    """Список объявлений"""
    queryset = Ad.objects.order_by('dt_created')
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


class FeedbacksList(LoginRequiredMixin, ListView):
    """Список отзывов на объявления пользователя"""
    model = Feedback
    template_name = 'feedbacks_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(ad__author__user=self.request.user).order_by('-id')
        self.filterset = FeedbackFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class FeedbackDelete(LoginRequiredMixin, DeleteView):
    """Удалить отзыв"""
    model = Feedback
    template_name = 'feedback_delete.html'
    success_url = reverse_lazy('feedbacks_list')


def accept_feedback(request, pk):
    """Принять отзыв"""
    if not request.user or not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.accepted = True
    feedback.save()

    return redirect(reverse('feedbacks_list'))


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


def left_feedback(request, pk):
    """Оставить отзыв на объявление"""
    ad = get_object_or_404(Ad, pk=pk)

    if request.method == 'POST':
        Feedback.objects.create(content=request.POST['content'], ad=ad, author=request.user)

    return redirect(reverse('ad_detail', args=(pk,)))
