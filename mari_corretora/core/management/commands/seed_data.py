from django.core.management.base import BaseCommand
from core.models import SiteConfig


class Command(BaseCommand):
    help = "Cria dados iniciais para o site"

    def handle(self, *args, **options):
        if not SiteConfig.objects.exists():
            SiteConfig.objects.create(
                site_name="Mari Corretora",
                whatsapp_number="+554788562089",
                phone="(47) 8856-2089",
                email="contato@maricorretora.com.br",
                address="Porto Belo - SC, Brasil",
                hero_title="Imóveis de Alto Padrão em Porto Belo e Itapema",
                hero_subtitle="Exclusividade e sofisticação no litoral catarinense",
                hero_cta_text="Fale com Mari no WhatsApp",
                about_title="Por que investir aqui",
                about_text=(
                    "Porto Belo e Itapema são os destinos que mais crescem em Santa Catarina, "
                    "com valorização imobiliária acima da média nacional. "
                    "A região oferece infraestrutura de ponta, belezas naturais exuberantes "
                    "e uma qualidade de vida incomparável.\n\n"
                    "Com empreendimentos como o Complexo Neymar, Senna Tower e o novo "
                    "Hard Rock Café Itapema, a região se consolida como o principal polo "
                    "de luxo do sul do Brasil."
                ),
                instagram_url="https://instagram.com/maricorretora",
                facebook_url="https://facebook.com/maricorretora",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS("Configuração inicial criada com sucesso!"))
        else:
            self.stdout.write(self.style.WARNING("Configuração já existe. Nenhuma ação necessária."))
