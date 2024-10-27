from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
# Create your models here.
# Change form register django

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.user.username


class Create_User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Your name', 
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Your email',
                'required': 'required'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input-field', 
                'placeholder': 'First name', 
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Last name', 
                'required': 'required'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Password',
                'required': 'required'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Repeat your password',
                'required': 'required'
            }),
        }
        
        


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name_seller = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(default=0.0)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True)
    detail = models.TextField(null=True,blank=True)
    seller = models.CharField(max_length=200,null=True,)
    Hotline = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.name or 'No name'
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = '/medias/placeholder.png'
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.customer)
    @property
    # đếm số lượng sản phẩm mua 
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    # tính tổng tiền
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)

    @property
    # tính tổng tiền trong item
    def get_total(self):
        if self.product is not None:
           total = self.product.price * self.quantity
        else:
            total = 0  # Nếu không có sản phẩm, trả về 0
        return total
    
class ShippingAddress(models.Model):
    # on_delete=models.CASCADE on_delete=models.CASCADE, điều này có nghĩa là nếu một sản phẩm bị xóa, tất cả các mục trong OrderItem liên kết với sản phẩm đó cũng sẽ tự động bị xóa.
    customer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return f'Shipping Address for {self.customer.username}'
    
class Post(models.Model):
    poster = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,blank=True)
    video = models.FileField(null=True,blank=True)
    likes = models.ManyToManyField(User,related_name='post_likes', blank = True)

    def __str__(self):
        return str(self.id)
    def number_of_likes(self):
        return self.likes.count()
    
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(null=True,blank=True)
    
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Reply(models.Model):
    parent_comment= models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return f"Response {self.parent_comment.author}"

class Buyed(models.Model) :
    buyed_product = models.ForeignKey(OrderItem,on_delete=models.CASCADE)

   
    
