from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo
#generic view를 상속받아서 구현.

class PhotoList(ListView):
	model = Photo
	template_name_suffix = '_list' # name_suffix : django가 특정네임값을 찾아감.


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

from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

class PhotoLike(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated: #로그인이 안되어있으면
			return HttpResponseForbidden() #자료를 숨겨라
		else:
			if 'photo_id' in kwargs: #photo_id를 확인
				photo_id = kwargs['photo_id'] #photo_id로 할당
				photo = Photo.objects.get(pk=photo_id)
				user = request.user
				if user in photo.like.all(): #좋아요를 누른경우
					photo.like.remove(user)  #좋아요가 사라짐.
				else:
					photo.like.add(user)

			referer_url = request.META.get('HTTP_REFERER')
			#성공했을 때 어떤 url로 이동할지 결정
			path = urlparse(referer_url).path
			#url을 분석해서
			return HttpResponseRedirect(path)
			#다시 그 url로 돌아옴.
		
class PhotoFavorite(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		else:
			if 'photo_id' in kwargs:
				photo_id = kwargs['photo_id']
				photo = Photo.objects.get(pk=photo_id)
				user = request.user
				if user in photo.favorite.all():
					photo.favorite.remove(user)
				else:
					photo.favorite.add(user)

			referer_url = request.META.get('HTTP_REFERER')
			path = urlparse(referer_url).path
			return HttpResponseRedirect(path)
		