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
        "bg": "/static/core/images/presentation/senna-tower.jpg",
        "title": "Atuação em Santa Catarina",
        "text": "Há 2 anos atuo no litoral norte de Santa Catarina, uma das regiões mais valorizadas e desejadas do Brasil, acompanhando de perto o crescimento acelerado do mercado imobiliário local. Aqui na região está sendo construído o Senna Tower, o maior prédio residencial do mundo, em Balneário Camboriú.",
    },
    {
        "image": "core/images/presentation/slide-04.jpeg",
        "bg": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80",
        "title": "Minha especialidade",
        "text": "🏡 Especialista em imóveis na planta e apartamentos prontos de médio e alto padrão.\n\nAuxilio clientes que desejam investir com segurança, preservar patrimônio ou conquistar um imóvel alinhado ao seu estilo de vida.",
    },
    {
        "image": "core/images/presentation/slide-01.jpeg",
        "bg": "/static/core/images/presentation/hard-rock-itapema.jpg",
        "title": "Itapema",
        "text": "📈 Atuo em Itapema, referência nacional em valorização imobiliária, qualidade de vida e forte potencial de rentabilidade para investidores. A cidade conta agora com o Píer Oporto e o Hard Rock Cafe Itapema, a única unidade da rede construída sobre a água no mundo.",
    },
    {
        "image": "core/images/presentation/slide-03.jpeg",
        "bg": "/static/core/images/presentation/charles-ii.jpg",
        "title": "Charles II Yacht Royal Home",
        "text": "⛵ O Charles II Yacht Royal Home by OKEAN é o primeiro branded residence náutico da América Latina, em Itapema. Inspirado no iate OKEAN 80, terá 255 m de altura, mais de 70 pavimentos, marina privativa com atracadouro, heliponto homologado e o Sky Place com piscina de borda infinita com vista de 180° do mar. Um marco do luxo náutico no litoral catarinense.",
    },
    {
        "image": "core/images/presentation/slide-01.jpeg",
        "bg": "/static/core/images/presentation/edify-one.jpg",
        "title": "Edify One",
        "text": "🏗️ O Edify One, em Itapema, é o 'prédio do Neymar', com 45 pavimentos e cobertura triplex de R$ 52 milhões. Conta com heliponto homologado, 2.700 m² de área de lazer com piscina infinita, academia, spa e vista frente mar. Um empreendimento que redefine o padrão de luxo na cidade.",
    },
    {
        "image": "core/images/presentation/slide-02.jpeg",
        "bg": "/static/core/images/presentation/ecossistema-neymar.jpg",
        "title": "Porto Belo",
        "text": "🌊 Também atuo em Porto Belo, cidade que vem atraindo grandes investimentos, novos empreendimentos e marcas de relevância internacional, consolidando-se como uma das regiões mais promissoras do país. A cidade receberá o Ecossistema Neymar Jr., megacomplexo esportivo e de luxo.",
    },
    {
        "image": "core/images/presentation/slide-03.jpeg",
        "bg": "/static/core/images/presentation/emaar-exclusive.jpg",
        "title": "Emaar Exclusive",
        "text": "✨ O Emaar Exclusive, em Porto Belo, é um empreendimento de alto padrão que oferece apartamentos com acabamentos premium, vista para o mar e áreas de lazer completas. Uma oportunidade única de morar em uma das regiões mais valorizadas de Santa Catarina.",
    },
    {
        "image": "core/images/presentation/slide-04.jpeg",
        "bg": "/static/core/images/presentation/gran-paradiso.jpg",
        "title": "Gran Paradiso",
        "text": "🌿 O Gran Paradiso, em Porto Belo, é um residencial de luxo cercado por natureza, com apartamentos amplos, áreas verdes preservadas e infraestrutura completa de lazer. O equilíbrio perfeito entre sofisticação e contato com a natureza.",
    },
    {
        "image": "core/images/presentation/slide-03.jpeg",
        "bg": "/static/core/images/presentation/all-resort-portobelo.jpg",
        "title": "All Resort Club Residence",
        "text": "🏌️ O All Resort Club Residence, em Porto Belo, é o maior resort residencial da Costa Esmeralda, com campo de golfe iluminado (único da América Latina), Rafa Nadal Tennis Center, piscina de ondas com 1km de praia artificial, centro hípico e o Park Art Design com obras de arquitetura a céu aberto. Um marco do luxo e da qualidade de vida na região.",
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
