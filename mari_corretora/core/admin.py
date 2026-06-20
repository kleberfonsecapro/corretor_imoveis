from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, CarouselImage, Property, PropertyImage, Testimonial


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ["image", "alt_text", "is_main", "order", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Prévia"


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ["site_name", "whatsapp_number", "is_active"]


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active", "image_preview", "created_at"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active"]
    fields = ["title", "caption", "image", "order", "is_active", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Prévia"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "title", "city", "property_type",
        "price_display", "is_featured", "is_active",
        "main_image_preview",
    ]
    list_filter = ["is_featured", "is_active", "property_type", "city"]
    list_editable = ["is_featured", "is_active"]
    search_fields = ["title", "description", "address"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [PropertyImageInline]
    fieldsets = [
        ("Informações Básicas", {"fields": ["title", "slug", "description", "short_description", "property_type"]}),
        ("Localização", {"fields": ["address", "neighborhood", "city", "state"]}),
        ("Detalhes", {"fields": ["price", "bedrooms", "suites", "bathrooms", "garage_spots", "area", "total_area"]}),
        ("Status", {"fields": ["is_featured", "is_active"]}),
    ]

    def price_display(self, obj):
        if obj.price:
            return f"R$ {obj.price:,.0f}".replace(",", ".")
        return "-"

    price_display.short_description = "Preço"

    def main_image_preview(self, obj):
        main = obj.main_image
        if main and main.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 4px;" />',
                main.image.url,
            )
        return "-"

    main_image_preview.short_description = "Foto"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "rating", "is_active", "photo_preview", "created_at"]
    list_filter = ["is_active", "rating"]
    list_editable = ["is_active"]
    fields = ["name", "photo", "text", "rating", "is_active", "photo_preview"]
    readonly_fields = ["photo_preview"]

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 50%;" />',
                obj.photo.url,
            )
        return format_html(
            '<div style="width: 80px; height: 80px; border-radius: 50%; '
            'background: #1a2744; display: flex; align-items: center; '
            'justify-content: center; color: white; font-size: 32px;">{}</div>',
            obj.name[0].upper() if obj.name else "?",
        )

    photo_preview.short_description = "Foto"
