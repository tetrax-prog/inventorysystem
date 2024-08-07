from django.db import models
from django.contrib.auth.models import User


CATEGORY = (
    ('Stationary','Stationary'),
    ('Electronics','Electronics'),
    ('Food','Food'),
)
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=20,blank=True, null=True)
    quantity = models.PositiveIntegerField(null=True)
    export_to_CSV = models.BooleanField(default=False)

    class Meta:
       verbose_name_plural = 'Product'

    def __str__(self):
      
      return f'{self.name}-{self.quantity}'
    
class Order(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   staff = models.ForeignKey(User, models.CASCADE, null=True)
   order_quantity = models.PositiveBigIntegerField(null=True)
   date = models.DateTimeField(auto_now_add=True)

   class Meta:
       verbose_name_plural = 'Order'

   def __str__(self):
      
      return f'{self.product} ordered by {self.staff.username}'
