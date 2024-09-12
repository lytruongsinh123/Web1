from django.contrib import admin
from django.urls import path
from . import views
from .views import delete_product
from django.views.generic import ListView
from .models import *
urlpatterns = [
    path('', views.home, name="home"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/', views.UpdateItem, name="update_item"),
    path('register/', views.Register, name = "register"),
    path('login/', views.Login, name = "login"),
    path('search', views.search, name="search"),
    path('logout/',views.Logout, name="logout"),
    path('category/',views.Categoris,name="category"),
    path('detail/',views.Detail, name = "detail" ),
    path('seller/',views.Seller_infor, name = "seller"),
    path('individual', views.Infor_Individual, name = 'individual'),
    path('postproduct/', views.PostProducts, name = 'postproduct'),
    path('postblog/', views.postblog, name = "postblog"),
    path('blog/', ListView.as_view(

      queryset = Post.objects.all().order_by('-date'),
      template_name = 'app/blog.html',
      context_object_name = 'Posts',
      paginate_by = 10)
      ,name='blog'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),  
    path('app/<int:id>/',views.post, name = 'post'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_reply/', views.add_reply, name='add_reply'),
    path('test/', views.test, name='test'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
]
