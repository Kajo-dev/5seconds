
from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from user_log_reg.models import Profile
from product_store.models import Cart, CartItem

@login_required(login_url='login_page')
def product_sell(request):
    products = Product.objects.all() 
    for_front = {'products':products}
    return render(request,'sellsite.html',for_front)

@login_required(login_url='login_page')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    sizes = Sizes.objects.filter(id_product=product)
    for_front = {
        'product':product,
        'sizes':sizes
    }
    return render(request, 'detail_product.html', for_front)

@login_required(login_url='login_page') 
def my_orders(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=user_profile)
    for_front={
        'user_cart' : cart
    }
    return render(request,'my_orders.html', for_front)


@login_required(login_url='login_page') 
def my_cart(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    user_cart = Cart.objects.filter(owner=user_profile)
    for_front={
        'user_cart' : user_cart
    }
    return render(request,'cart.html', for_front)

@login_required(login_url='login_page')
def add_to_cart(request,**kwargs):
    user_profile = get_object_or_404(Profile,user=request.user)
    product = Product.objects.filter(id=kwargs.get('product_id', "")).first()   
    cart_item, status = CartItem.objects.get_or_create(product=product)
    user_cart, status = Cart.objects.get_or_create(owner=user_profile)
    user_cart.items.add(cart_item)
    if status:
        user_cart.save()

    return redirect('sellsite_page')


@login_required()
def delete_from_cart(request, **kwargs):
    item_to_delete = CartItem.objects.filter(pk=kwargs.get('items_id', "")).first()
    if not item_to_delete == None:
        item_to_delete.delete()
    return redirect('cart_page')