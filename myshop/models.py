from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myshop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    name = name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    slug = slug = models.SlugField(max_length=200, unique=True, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-created_on',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myshop:product_detail', args=[self.slug, self.id])

    def get_add_to_cart_url(self):
        return reverse('myshop:add_to_cart', args=[self.slug, self.id])

    def get_remove_from_cart_url(self):
        return reverse('myshop:remove_from_cart', args=[self.slug, self.id])

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.quantity} of {self.product}"

    def get_total_order_price(self):
        return self.quantity * self.product.price

    def get_total_discount_order_price(self):
        return self.quantity * self.product.discounted_price

    def get_amount_saved(self):
        return self.get_total_order_price() - self.get_total_discount_order_price()

    def get_final_price (self):
        if self.product.discounted_price:
            return self.get_total_discount_order_price()
        return self.get_total_order_price()

    class Meta:
        verbose_name = 'Your Order'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True )
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total
