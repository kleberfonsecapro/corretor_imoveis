from django.shortcuts import render
from .models import SiteConfig, CarouselImage, Property, Testimonial


def home(request):
    config = SiteConfig.objects.filter(is_active=True).first()
    carousel_images = CarouselImage.objects.filter(is_active=True)
    featured_properties = Property.objects.filter(
        is_active=True, is_featured=True
    ).prefetch_related("images")[:6]
    testimonials = Testimonial.objects.filter(is_active=True)

    context = {
        "config": config,
        "carousel_images": carousel_images,
        "featured_properties": featured_properties,
        "testimonials": testimonials,
    }
    return render(request, "core/index.html", context)
