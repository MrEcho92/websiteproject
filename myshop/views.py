from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, View, )
from django.shortcuts import get_object_or_404
from django.utils import timezone
from myshop.models import Product, Category, Order, OrderProduct
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def product_list(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render (request, 'product_list.html', {'category': category,
                                                    'categories': categories,
                                                    'products': products})

    def listing(request):
        product_list = products
        paginator = Paginator(product_list, 10) # Show 10 blogs per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product_list.html', {'page_obj': page_obj})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    #cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {'product': product, })

@login_required
def add_to_cart(request,id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "Item quantity updated to your cart.")
            return redirect("myshop:order-summary")
        else:
            messages.info(request, "Item added to your cart.")
            order.products.add(order_product)
            return redirect("myshop:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user= request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "Item was added to your cart.")
    return redirect("myshop:order-summary")

@login_required
def remove_from_cart(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            messages.info(request, "Item removed from your cart.")
            return redirect("myshop:order-summary")
        else:
            messages.info(request, "Item not in your cart.")
            return redirect("myshop:product_detail",id=id, slug=slug)

    else:
        messages.info(request, "No active order..")
        return redirect("myshop:product_detail",id=id, slug=slug)
    return redirect("myshop:product_detail",id=id, slug=slug)


@login_required
def remove_single_product_from_cart(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity >1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "Item quantity updated")
        return redirect("myshop:order-summary")
    else:
        messages.info(request, "No active order..")
        return redirect("myshop:product_detail", id=id, slug=slug)
    return redirect("myshop:product_detail", id=id, slug=slug)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
            'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'No active orders..')
            return redirect ("/")
