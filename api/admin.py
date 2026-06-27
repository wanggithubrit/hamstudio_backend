from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Product, Collection, FaqItem, Order, ContactMessage, SiteSetting, SocialFeedItem

class HamAdminSite(AdminSite):
    site_header = "HAM STUDIO Admin Dashboard"
    site_title = "HAM STUDIO Portal"
    index_title = "Website Management Control Center"

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        
        try:
            orders = Order.objects.all()
            total_sales = 0
            for o in orders:
                items = o.items
                if isinstance(items, list):
                    for item in items:
                        try:
                            price = float(item.get('price', 0))
                        except (ValueError, TypeError):
                            price = 0.0
                        try:
                            qty = float(item.get('quantity', 1))
                        except (ValueError, TypeError):
                            qty = 1.0
                        total_sales += price * qty
            
            extra_context['total_sales'] = f"{int(total_sales):,}"
            extra_context['total_orders'] = orders.count()
            extra_context['total_messages'] = ContactMessage.objects.count()
            extra_context['total_products'] = Product.objects.count()
        except Exception:
            pass

        return super().index(request, extra_context)

admin_site = HamAdminSite(name='ham_admin')

# Register auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Register models on custom admin site
@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'tag')
    search_fields = ('name', 'category', 'description')

@admin.register(Collection, site=admin_site)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tag')
    search_fields = ('name',)

@admin.register(FaqItem, site=admin_site)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    search_fields = ('question',)

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('orderId',)

@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('name', 'email', 'subject')

@admin.register(SiteSetting, site=admin_site)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'description')

@admin.register(SocialFeedItem, site=admin_site)
class SocialFeedItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'image', 'image_url')
    search_fields = ('alt_text',)
