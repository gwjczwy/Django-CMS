from django.urls import path
from . import views

app_name='posting'
urlpatterns=[
    path('posting/',views.index,name='index'),
    path('posting/createposting/',views.createPosting), #发帖
    path('posting/createcomment/<int:postId>',views.createComment), #发帖
    path('posting/<str:postTitle>/',views.getPostByTitle), #查看帖子

]