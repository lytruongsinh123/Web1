import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .forms import CommentForm
from .models import *


def Detail(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get("id", "")
    product = Product.objects.filter(id=id)
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
        "product": product,
    }
    return render(request, "app/detail.html", context)


def Categoris(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get("category", "")
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {
        "categories": categories,
        "products": products,
        "active_category": active_category,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
    }
    return render(request, "app/category.html", context)


def search(request):
    categories = Category.objects.filter(is_sub=False)
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__icontains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cartItems,
        "searched": searched,
        "keys": keys,
        "categories": categories,
    }
    return render(request, "app/search.html", context)


def Register(request):
    user_not_login = "show"
    user_login = "hidden"
    form = Create_User_Form()
    if request.method == "POST":
        form = Create_User_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Trả về trang web login
    context = {"form": form, "user_not_login": user_not_login, "user_login": user_login}
    return render(request, "app/register.html", context)


def Login(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:

        return redirect("home")
    else:
        user_not_login = "show"
        user_login = "hidden"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Trả về trang web home
        else:
            messages.info(request, "Name or password not correct!")
    context = {
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
    }
    return render(request, "app/login.html", context)


def Logout(request):
    """logout(request)
    return redirect('login')"""  # Trả về trang web login
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")
    else:
        return redirect("home")


def home(request):
    try:
        latest_post = Post.objects.latest("date")
    except ObjectDoesNotExist:
        latest_post = None

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub=False)

    products = Product.objects.all()
    context = {
        "products": products,
        "latest_post": latest_post,
        "cartItems": cartItems,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
    }
    return render(request, "app/home.html", context)


def cart(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
    }
    return render(request, "app/cart.html", context)


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def Seller_infor(request):
    return render(request, "app/seller_infor.html")


def checkout(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"

    # Kiểm tra xem thông tin liên hệ đã tồn tại chưa
    contact_infos = ShippingAddress.objects.filter(customer=request.user).first()

    if request.method == "POST":
        form = ContactInfoForm(request.POST, instance=contact_infos)
        if form.is_valid():
            contact_infos = form.save(commit=False)
            contact_infos.customer = request.user
            contact_infos.save()
            return render(
                request,
                "app/checkout.html",
                {
                    "items": items,
                    "form": form,
                    "order": order,
                    "cartItems": cartItems,
                    "user_not_login": user_not_login,
                    "user_login": user_login,
                    "categories": categories,
                    "submitted": True,  # Đánh dấu form đã được submit và hợp lệ
                },
            )
    else:
        # Load form với dữ liệu đã lưu (nếu có)
        form = ContactInfoForm(instance=contact_infos)
    
    if request.method == "POST":
        order_items = OrderItem.objects.all()
        for item in order_items:
            if item:
                try:
                    Buyed.objects.create(buyed_product=item.product)
                except Exception as e:
                    print(f"Lỗi khi tạo Buyed: {e}")
        return redirect('home')
        

    context = {
        "items": items,
        "form": form,
        "order": order,
        "cartItems": cartItems,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
        "submitted": contact_infos is not None,  # Kiểm tra nếu đã có thông tin lưu trữ
    }

    return render(request, "app/checkout.html", context)



def Infor_Individual(request):

    if request.user.is_authenticated:
        customer = request.user
        infor, created = ShippingAddress.objects.get_or_create(customer=customer)
        products = Product.objects.filter(name_seller=customer)
        context = {
            "infor": infor,
            "products": products,
        }

    return render(request, "app/Individual.html", context)


@login_required(
    login_url="login"
)  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
def PostProducts(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"

    if request.method == "POST":
        forms = Post_Products_Form(request.POST, request.FILES)
        if forms.is_valid():
            product = forms.save(
                commit=False
            )  # Lưu đối tượng chính mà chưa lưu ManyToMany
            product.name_seller = request.user  # Gán người dùng hiện tại
            product.save()  # Lưu đối tượng chính
            forms.save_m2m()  # Lưu các quan hệ ManyToMany, như 'category'

            return redirect("home")
    else:
        forms = Post_Products_Form()

    context = {
        "forms": forms,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "categories": categories,
        "user_not_login": user_not_login,
        "user_login": user_login,
    }
    return render(request, "app/postproduct.html", context)


# def list(request):
#    Data = {'Posts': Post.objects.all().order_by('-date')}
#    return render(request, 'app/blog.html', Data) 


# def post(request, id):
#     post = Post.objects.get(id=id)
#     return render(request, 'app/post.html', {'post': post}) 

# class PostListView(ListView):
#     queryset = Post.objects.all().order_by('-date')
#     template_name = 'app/blog.html'
#     context_object_name = 'Posts'
#     paginate_by = 10


def post(request, id, comment_id=None):
    post = get_object_or_404(Post, id=id)
    comment = None
    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id, post=post)

    liked = False
    # Kiểm tra nếu người dùng đã like bài viết và đăng nhập
    if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

    
    form = CommentForm()
    if request.method == "POST":    
        form = CommentForm(request.POST, author=request.user, post=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path) # Không bị lặp lại yêu cầu khi load lại trang web 
        
    

    context = {"post": post, 
               "form": form, 
               "comment": comment,
               "liked": liked}
    return render(request, "app/post.html", context)


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def postblog(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"

    if request.method == "POST":
        forms = Post_Products_Form(request.POST, request.FILES)
        if forms.is_valid():
            product = forms.save(
                commit=False
            )  # Lưu đối tượng chính mà chưa lưu ManyToMany
            product.name_seller = request.user  # Gán người dùng hiện tại
            product.save()  # Lưu đối tượng chính
            forms.save_m2m()  # Lưu các quan hệ ManyToMany, như 'category'

            return redirect("home")
    else:
        forms = Post_Products_Form()

    if request.method == "POST":
        formss = Post_Blog(request.POST, request.FILES)
        if formss.is_valid():
            new_post = formss.save(commit=False)
            new_post.poster = request.user  # Gán poster là người đang đăng nhập
            new_post.save()

            return redirect("home")
            # redirect hoặc xử lý tiếp
    else:
        formss = Post_Blog()

    context = {
        "forms": forms,
        "formss": formss,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "categories": categories,
        "user_not_login": user_not_login,
        "user_login": user_login,
    }
    return render(request, "app/postblog.html", context)


def add_comment(request):
    
    if request.method == "POST":
        print(request.POST)  # In ra dữ liệu POST để kiểm tra
        post_id = request.POST.get("post_idd") # Lấy id bài viết từ form <input type="hidden" name="post_idd" value="{{ post.id }}" /> (post.html)
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST, author=request.user, post=post)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Comment added successfully!"})
        else:
            return JsonResponse({"errors": "Comment added failed!"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def add_reply(request):
    if request.method == "POST":
        print(request.POST)
        comment_id = request.POST.get("comment_idd")
        parent_comment = get_object_or_404(Comment, id=comment_id)
        formss = ReplyForm(request.POST, author = request.user, parent_comment = parent_comment)

        if formss.is_valid():
            formss.save()
            return JsonResponse({"message": "Comment added successfully!"})
        else:
            return JsonResponse({"errors": formss.errors.as_json()}, status=400)
        
    return JsonResponse({"error": "Invalid request"}, status=400)

    
def blog(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()

    context = {
        "products": products,
        "items": items,
        "cartItems": cartItems,
        "user_not_login": user_not_login,
        "user_login": user_login,
        "categories": categories,
    }
    return render(request, "app/blog.html", context)


def test(request):
    user_not_login = "show"
    user_login = "hidden"
    form = Create_User_Form()
    if request.method == "POST":
        form = Create_User_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Trả về trang web login
    context = {"form": form, "user_not_login": user_not_login, "user_login": user_login}
    return render(request, "app/test.html", context)


# view để xóa sản phẩm
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, name_seller=request.user)  # lấy sản phẩm có product_id =id và name_seller = người đăng nhập hiện tại
    if request.method == "POST":
        product.delete()
        return redirect("home")  # Chuyển hướng đến trang danh sách sản phẩm sau khi xóa

    return render(request, "app/confirm_delete.html", {"product": product})

def buyed_product(request):
    buyed_product = Buyed.objects.all() # Lấy tất cả các Buyed để hiển thị
    context = {"buyed_product": buyed_product}
    return render(request, 'app/buyed.html', context)

   