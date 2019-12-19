from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Photo(models.Model):
	#User는 django에서 지원해주는것을 가져옴.
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user') #작성자
	#ForeignKey를 통해서 User를 연결
	
	text = models.TextField(blank=True) #텍스트
	image = models.ImageField(upload_to = 'timeline_photo/%Y/%m/%d') #이미지 알아서 시간 설정해서 저장
	created = models.DateTimeField(auto_now_add=True) #생성일
	update = models.DateTimeField(auto_now=True) #수정일


	like=models.ManyToManyField(User, related_name='like_post', blank=True)
	favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

	def __str__(self):
		return "text : "+self.text

	class Meta: #models.Model을 상속 받아와서 안에 내용을 바꿔줌
		ordering = ['-created']

	def get_absolute_url(self):
		return reverse('photo:detail', args=[self.id])
