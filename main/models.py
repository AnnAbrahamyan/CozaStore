from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Image(models.Model):
    img = models.ImageField('Image', upload_to='media')


class Size(models.Model):
    size = models.CharField('Size', max_length=15)

    def __str__(self) -> str:
        return self.size


class Color(models.Model):
    color = models.CharField('Color', max_length=20)

    def __str__(self) -> str:
        return self.color


class Quantity(models.Model):
    quantity = models.PositiveSmallIntegerField('Quantity')

    def __str__(self) -> str:
        return f'{self.quantity}'


def get_last_product_code_default():
    last_instance = Product.objects.last()
    if last_instance:
        return last_instance.code + 1
    return 1 


class ClothingOwnerDetector(models.Model):
    OWNER_DETECTOR_CHOICES = [
        ('women', 'women'),
        ('men', 'men'),
        ('mag', 'mag'),
        ('shoes', 'shoes'),
        ('watches', 'watches'),
    ]

    owner_detector = models.CharField('Type', max_length=15, choices=OWNER_DETECTOR_CHOICES)

    def __str__(self) -> str:
        return self.owner_detector


class ClothingType(models.Model):
    type = models.CharField('Clothing Type', max_length=150)

    def __str__(self) -> str:
        return self.type

class Product(models.Model):
    product_name = models.CharField('Product Name', max_length=150)
    img = models.ManyToManyField('Image')
    description = models.TextField('Description', default='Aenean sit amet gravida nisi. Nam fermentum est felis, quis feugiat nunc fringilla sit amet. Ut in blandit ipsum. Quisque luctus dui at ante aliquet, in hendrerit lectus interdum. Morbi elementum sapien rhoncus pretium maximus. Nulla lectus enim, cursus et elementum sed, sodales vitae eros. Ut ex quam, porta consequat interdum in, faucibus eu velit. Quisque rhoncus ex ac libero varius molestie. Aenean tempor sit amet orci nec iaculis. Cras sit amet nulla libero. Curabitur dignissim, nunc nec laoreet consequat, purus nunc porta lacus, vel efficitur tellus augue in ipsum. Cras in arcu sed metus rutrum iaculis. Nulla non tempor erat. Duis in egestas nunc.')
    type = models.ForeignKey(ClothingType, on_delete=models.CASCADE, related_name='type_rn', null=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, related_name='color_rn')
    size = models.ManyToManyField('Size')
    quantity = models.ManyToManyField('Quantity')
    price = models.DecimalField('Price', max_digits=5, decimal_places=2)
    weight = models.FloatField('Weight (kg)', default=0.8)
    dimensions = models.CharField('Dimensions (cm)', max_length=150, default='110 x 33 x 100')
    material = models.CharField('Material', max_length=150, default='60% cotton')
    code = models.PositiveSmallIntegerField('Code', default=get_last_product_code_default)
    owner_detector = models.ForeignKey(ClothingOwnerDetector, on_delete=models.CASCADE, related_name='owner_detector_rn')
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.img.set(self.img.all())
        self.size.set(self.size.all())
        self.quantity.set(self.quantity.all())


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


class ContactSubmission(models.Model):
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    


class LikedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField('Price', max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.product} ({self.size}, {self.color}) x {self.quantity}'





class ShippingInformation(models.Model):
    shipping_info = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipping Info - {self.country} {self.zip_code}"

