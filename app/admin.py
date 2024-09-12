from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ContactInfoAdmin(admin.ModelAdmin):
    form = ContactInfoForm

class Post_Products_Form_Admin(admin.ModelAdmin):
    form = Post_Products_Form
    list_display = ['name', 'seller','image','display_categories','name_seller']

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])

    display_categories.short_description = 'Categories'  # Đặt tên cho cột

    # obj.category.all(): Lấy tất cả các đối tượng Category liên quan đến sản phẩm hiện tại (dùng với ManyToManyField).
    # category.name for category in obj.category.all(): Lặp qua tất cả các danh mục và lấy tên của từng danh mục.
    # ", ".join([...]): Nối các tên danh mục thành một chuỗi, ngăn cách nhau bởi dấu phẩy (,)

class PostAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_order']

class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin1(admin.ModelAdmin):
    form = Post_Blog
    list_display = ['title', 'date', 'image_thumbnail', 'video','poster']
    list_filter = ['date']
    search_fields = ['title', 'id']
    inlines = [CommentInline]

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" style="height: 100px;" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_thumbnail.allow_tags = True


class UserProfileAdmin(admin.ModelAdmin):
     list_display = ['user', 'image']  
     search_fields = ['user__username']
admin.site.register(Profile, UserProfileAdmin)
    

class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    # nếu không có đoạn code này thì không thể add user
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

    
admin.site.unregister(User) 
admin.site.register(User,UserAdmin)
admin.site.register(Category)
admin.site.register(Product, Post_Products_Form_Admin)
admin.site.register(Order, PostAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress, ContactInfoAdmin)
admin.site.register(Post, PostAdmin1)
admin.site.register(Reply) 

