from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Camera, UserProfile
from .forms import SignUpForm

import re
import uuid

# Create your views here.
def index(request):
    return render(request, 'camapp/index.html')

@login_required
def me(request):
    profile = UserProfile.objects.filter(user=request.user)[0]
    cameras = Camera.objects.filter(user=request.user)
    context = {
        'cameras': cameras,
        'profile': profile,
    }
    return render(request, 'camapp/me.html', context=context)

@never_cache
def frame_view(request, pk):
    if request.method == 'GET':
        obj = get_object_or_404(Camera, pk=pk)
        api_key = UserProfile.objects.filter(user=obj.user)[0].api_key
        clean_id = [x for x in str(obj.id) if x != '-']
        clean_id = "".join(clean_id)
        context = {
            'camera_path': 'cameras/' + clean_id + '/index.m3u8',
        }
        
        if str(api_key) != request.GET.get('api_key', ''):
            return HttpResponseForbidden() 
        r = render(request, 'camapp/camera_frame.html', context)
        r['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return r
    else:
        return HttpResponseBadRequest

@login_required
def api_key(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    profile.api_key = str(uuid.uuid4())
    profile.save()
    return HttpResponseRedirect(reverse('me'))

class CameraDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Camera

    def test_func(self):
        # Test if user is an author
        obj = super().get_object()
        return self.request.user == obj.user or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        profile = UserProfile.objects.filter(user=self.request.user)[0]
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        context['frame_code'] = f'<iframe width="560" height="315" src="http://127.0.0.1:8000{self.request.path}/frame/?api_key={profile.api_key}" ' \
                                 'frameborder="0" gesture="media" allow="encrypted-media" allowfullscreen></iframe>'
        return context


class CameraCreate(LoginRequiredMixin, CreateView):
    model = Camera
    fields = ['alias', 'rtsp']
    initial = {'alias': 'My Camera', 'rtsp': 'rtsp://'}
    success_url = reverse_lazy('me')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CameraUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Camera
    fields = ['alias', 'rtsp']

    def test_func(self):
        # Test if user is an author
        obj = super().get_object()
        return self.request.user == obj.user or self.request.user.is_staff

    def clean_rtsp(self):
        data = self.cleaned_data['rtsp']
        if not re.match(r'(^(http|https|rtsp):\/\/\w+)', data):
            raise ValidationError(_('Invalid camera URL'))
        return data


class CameraDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Camera
    success_url = reverse_lazy('me')

    def test_func(self):
        # Test if user is an author
        obj = super().get_object()
        return self.request.user == obj.user or self.request.user.is_staff