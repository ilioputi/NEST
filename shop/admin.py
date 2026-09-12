
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'has_description')
    search_fields = ('name',)
    list_filter = ('price',)

    fieldsets = (
        ("Основное", {
            "fields": ("name", "price", "image_url"),
            "description": "Базовые данные о товаре."
        }),
        ("Описание", {
            "fields": ("description",),
            "classes": ("collapse",),
            "description": "Полное описание товара (отображается в модальном окне)."
        }),
    )

    def image_tag(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" style="border-radius: 4px; border: 1px solid #ddd;" />', obj.image_url)
        return format_html('<span style="color: #999;">{}</span>', 'Нет картинки')
    image_tag.short_description = 'Картинка'

    def has_description(self, obj):
        if obj.description and obj.description.strip():
            return format_html('<span style="color: #10b981;">{}</span>', '✓ Есть')
        return format_html('<span style="color: #ef4444;">{}</span>', '— Нет')
    has_description.short_description = 'Есть описание?'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total')
    readonly_fields = ('total',)

    def total(self, obj):
        return f"{obj.product.price * obj.quantity} ₽"
    total.short_description = 'Итого'