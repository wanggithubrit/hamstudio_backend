from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    original_price = models.IntegerField(null=True, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100)
    image = models.FileField(upload_to='products/', blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback image path/URL")
    meta = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    images = models.JSONField(default=list)

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

class Collection(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='collections/', blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback image path/URL")

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

class FaqItem(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    bullets = models.JSONField(default=list)

    def __str__(self):
        return self.question

class Order(models.Model):
    orderId = models.CharField(max_length=100, unique=True)
    items = models.JSONField()
    shipping = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Processing')

    def __str__(self):
        return self.orderId

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.TextField(blank=True, help_text="Text value or path/URL of the setting")
    image = models.FileField(upload_to='settings/', blank=True, null=True, help_text="Upload an image file directly (will override text value if set)")
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.key}: {self.get_value()[:50]}"

    def get_value(self):
        if self.image:
            return self.image.url
        return self.value

class SocialFeedItem(models.Model):
    image = models.FileField(upload_to='social/', blank=True, null=True, help_text="Upload an Instagram/social feed image directly")
    image_url = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback image path/URL if file is not uploaded")
    alt_text = models.CharField(max_length=255, default="HAM STUDIO curated sterling silver piece")

    def __str__(self):
        return f"Social Item {self.id}: {self.alt_text[:30]}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
