from django.db import models

# Create your models here.

class Product(models.Model):
    RATING_CHOICES = (
        ('G', 'Good'),
        ('B', 'Bad'),
        ('A', 'Average'),
        ('E', 'Excellent'),
    )

    product_title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    product_image = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
    price = models.PositiveIntegerField()
    product_availability = models.PositiveIntegerField()
    seller = models.CharField(max_length=500)
    product_warranty = models.PositiveIntegerField()
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)

    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.product_title