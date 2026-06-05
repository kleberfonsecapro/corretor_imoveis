from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import os


class SiteConfig(models.Model):
    site_name = models.CharField("Nome do Site", max_length=100, default="Mari Corretora")
    logo = models.ImageField("Logotipo", upload_to="logo/", blank=True, null=True)
    whatsapp_number = models.CharField("WhatsApp", max_length=20, default="+554788562089")
    phone = models.CharField("Telefone", max_length=20, blank=True)
    email = models.EmailField("E-mail", blank=True)
    address = models.CharField("Endereço", max_length=300, blank=True)
    hero_title = models.CharField("Título do Hero", max_length=200, default="Imóveis de Alto Padrão em Porto Belo e Itapema")
    hero_subtitle = models.CharField("Subtítulo do Hero", max_length=300, default="Exclusividade e sofisticação no litoral catarinense")
    hero_cta_text = models.CharField("Texto do Botão CTA", max_length=100, default="Fale com Mari no WhatsApp")
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    youtube_url = models.URLField("YouTube", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    about_title = models.CharField("Título 'Sobre'", max_length=200, default="Por que investir aqui")
    about_text = models.TextField("Texto 'Sobre'", blank=True)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return self.site_name


class CarouselImage(models.Model):
    title = models.CharField("Título", max_length=200, blank=True)
    caption = models.CharField("Legenda", max_length=300, blank=True)
    image = models.ImageField("Imagem", upload_to="carousel/")
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Imagem do Carrossel"
        verbose_name_plural = "Imagens do Carrossel"
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Carrossel #{self.pk}"


class Property(models.Model):
    STANDARD = "standard"
    LUXURY = "luxury"
    PENTHOUSE = "penthouse"
    COMMERCIAL = "commercial"
    LAND = "land"

    PROPERTY_TYPE_CHOICES = [
        (STANDARD, "Padrão"),
        (LUXURY, "Luxo"),
        (PENTHOUSE, "Cobertura"),
        (COMMERCIAL, "Comercial"),
        (LAND, "Terreno"),
    ]

    title = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=250, unique=True, blank=True)
    description = models.TextField("Descrição")
    short_description = models.CharField("Descrição curta", max_length=200, blank=True)
    property_type = models.CharField("Tipo", max_length=20, choices=PROPERTY_TYPE_CHOICES, default=LUXURY)
    address = models.CharField("Endereço", max_length=300, blank=True)
    neighborhood = models.CharField("Bairro", max_length=100, blank=True)
    city = models.CharField("Cidade", max_length=100, default="Porto Belo")
    state = models.CharField("Estado", max_length=50, default="SC")
    price = models.DecimalField("Preço", max_digits=15, decimal_places=2, blank=True, null=True)
    bedrooms = models.PositiveIntegerField("Quartos", blank=True, null=True)
    suites = models.PositiveIntegerField("Suítes", blank=True, null=True)
    bathrooms = models.PositiveIntegerField("Banheiros", blank=True, null=True)
    garage_spots = models.PositiveIntegerField("Vagas de garagem", blank=True, null=True)
    area = models.DecimalField("Área (m²)", max_digits=10, decimal_places=2, blank=True, null=True)
    total_area = models.DecimalField("Área total (m²)", max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField("Destaque", default=False)
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        ordering = ["-is_featured", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        first = self.images.filter(is_active=True).first()
        return first


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images", verbose_name="Imóvel"
    )
    image = models.ImageField("Imagem", upload_to="properties/")
    alt_text = models.CharField("Texto alternativo", max_length=200, blank=True)
    is_main = models.BooleanField("Principal", default=False)
    is_active = models.BooleanField("Ativo", default=True)
    order = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        verbose_name = "Foto do Imóvel"
        verbose_name_plural = "Fotos dos Imóveis"
        ordering = ["-is_main", "order"]

    def __str__(self):
        return f"Foto: {self.property.title}"

    def filename(self):
        return os.path.basename(self.image.name)


class Testimonial(models.Model):
    name = models.CharField("Nome", max_length=150)
    photo = models.ImageField("Foto", upload_to="testimonials/", blank=True, null=True)
    text = models.TextField("Depoimento")
    rating = models.PositiveIntegerField(
        "Avaliação",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )
    is_active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Depoimento de {self.name}"
