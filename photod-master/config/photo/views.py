from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo

class PhotoList(ListView):
	model = Photo
	template_name_suffix = '_list'


class PhotoCreate(CreateView):
	model = Photo
	fields = ['author','text', 'image']
	template_name_suffix = '_create'
	success_url = '/'

	def from_valid(self, form): 
		form.instance.author_id = self.request.user.id
		if form.is_valid():
			#올바르다면
			#form : 모델폼
			form.instance.save()
			return redirect('/')
		else:
			#올바르지 않다면
			return self.render_to_response({'form':form})

class PhotoUpdate(UpdateView):
	model = Photo
	fields = ['author','text', 'image']
	template_name_suffix = '_update'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		object = self.get_object()
		if object.author != request.user:
			messages.warning(request,'수정할 권한이 없습니다.')
			return HttpResponseRedirect('/')
		else:
			return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

from django.http import HttpResponseRedirect
from django.contrib import messages

class PhotoDelete(DeleteView):
	model = Photo
	template_name_suffix = '_delete'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		object = self.get_object()
		if object.author != request.user:
			messages.warning(request,'삭제할 권한이 없습니다.')
			return HttpResponseRedirect('/')
		else:
			return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
	model = Photo
	template_name_suffix = '_detail'