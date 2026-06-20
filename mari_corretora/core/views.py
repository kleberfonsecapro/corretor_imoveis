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


SLIDES = [
    {
        "image": "core/images/presentation/slide-01.jpeg",
        "bg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
        "title": "Apresentação",
        "text": "Especialista em imóveis de médio e alto padrão no litoral catarinense\n\nSou Mari Gomes, corretora de imóveis há 6 anos, dedicada a conectar pessoas às melhores oportunidades de moradia, investimento e valorização patrimonial.",
    },
    {
        "image": "core/images/presentation/slide-02.jpeg",
        "bg": "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1920&q=80",
        "title": "Minha trajetória",
        "text": "Natural de Cuiabá, Mato Grosso, construí minha base profissional atuando por 4 anos na capital mato-grossense, desenvolvendo experiência, credibilidade e conhecimento do mercado imobiliário.",
    },
    {
        "image": "core/images/presentation/slide-03.jpeg",
        "bg": "https://images.unsplash.com/photo-1505228395891-9a51e7e86bf6?w=1920&q=80",
        "title": "Atuação em Santa Catarina",
        "text": "Há 2 anos atuo no litoral norte de Santa Catarina, uma das regiões mais valorizadas e desejadas do Brasil, acompanhando de perto o crescimento acelerado do mercado imobiliário local.",
    },
    {
        "image": "core/images/presentation/slide-04.jpeg",
        "bg": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80",
        "title": "Minha especialidade",
        "text": "🏡 Especialista em imóveis na planta e apartamentos prontos de médio e alto padrão.\n\nAuxilio clientes que desejam investir com segurança, preservar patrimônio ou conquistar um imóvel alinhado ao seu estilo de vida.",
    },
    {
        "image": "core/images/presentation/slide-01.jpeg",
        "bg": "https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=1920&q=80",
        "title": "Itapema",
        "text": "📈 Atuo em Itapema, referência nacional em valorização imobiliária, qualidade de vida e forte potencial de rentabilidade para investidores.",
    },
    {
        "image": "core/images/presentation/slide-02.jpeg",
        "bg": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1920&q=80",
        "title": "Porto Belo",
        "text": "🌊 Também atuo em Porto Belo, cidade que vem atraindo grandes investimentos, novos empreendimentos e marcas de relevância internacional, consolidando-se como uma das regiões mais promissoras do país.",
    },
    {
        "image": "core/images/presentation/slide-03.jpeg",
        "bg": "https://images.unsplash.com/photo-1767449985562-013c41bd7fda?w=1920&q=80",
        "title": "Meu compromisso",
        "text": "Acredito que cada imóvel representa uma conquista e uma estratégia de futuro. Por isso, ofereço um atendimento consultivo, transparente e personalizado em todas as etapas da negociação.",
    },
    {
        "image": "core/images/presentation/slide-04.jpeg",
        "bg": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920&q=80",
        "title": "Convite",
        "text": "Se você busca oportunidades exclusivas em Itapema e Porto Belo, conte com quem conhece o mercado, acompanha as tendências e trabalha para encontrar o imóvel ideal para seus objetivos.\n\n\"Investir em imóveis é mais do que adquirir patrimônio. É construir um legado para o futuro.\" ✨🏙️🌊",
    },
]


def presentation(request):
    return render(request, "core/presentation.html", {"slides": SLIDES})
