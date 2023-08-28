from django.contrib import admin
from django.http.request import HttpRequest
from .models import *
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ("firstName","lastName", "email")

admin.site.register(Client, ClientAdmin)



class PaymentAdmin(admin.ModelAdmin):
    list_display = ("code", "deliveryAddress", "city", "comment")

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Payment, PaymentAdmin)

class PaymentsInCard(admin.TabularInline):
    model = Payment
    extra = 0

class CardAdmin(admin.ModelAdmin):
    list_display = ("cardNumber", "cardHolder")
    inlines = [PaymentsInCard]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
admin.site.register(Card, CardAdmin)

class ProductInShoppingCartInline(admin.TabularInline):
    model = ProductInShoppingCart
    extra = 1

class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [ProductInShoppingCartInline]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
admin.site.register(ShoppingCart, ShoppingCartAdmin)
