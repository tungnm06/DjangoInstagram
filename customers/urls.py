from django.urls import path, include
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('detail/<int:customer_id>', views.detail, name='detail'),
    path('upload/<int:customer_id>', views.upload, name='upload'),
    path('login', views.login, name='login'),
    path('newfeed/<int:customer_id>', views.newfeed, name='newfeed'),
    path('upload_avatar/<int:customer_id>', views.upload_avatar, name='upload_avatar'),
    path('<int:id_customer>/comments/<int:post_id>', views.comments, name='comments'),
    path('like_post', views.like_post, name='like_post'),
    path('like', views.like, name='like'),
    path('edit/<int:customer_id>', views.edit, name='edit'),
    path('editpass/<int:customer_id>', views.editpass, name='editpass'),
    path('edit_cmt', views.edit_cmt, name='edit_cmt'),
    path('search/<int:user_id>', views.search, name='search'),
    path('follow', views.follow, name='follow'),
    path('<int:user_id>/viewdetail/<int:customer_id>', views.viewdetail, name='detail'),
    path('<int:user_id>/postdetail/<int:post_id>', views.postdetail, name='postdetail'),
    path('logout', views.logout, name='logout'),

]
