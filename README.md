# Mari Corretora - Landing Page

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.1">
  <img src="https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL 8.4">
  <img src="https://img.shields.io/badge/Gunicorn-23.0-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn">
  <img src="https://img.shields.io/badge/Traefik-3-EE3D3D?style=for-the-badge&logo=traefikproxy&logoColor=white" alt="Traefik 3">
  <img src="https://img.shields.io/badge/Docker-24-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Jazzmin-2.6-1a2744?style=for-the-badge&logo=django&logoColor=white" alt="Jazzmin">
</p>

Landing page institucional para a corretora de imóveis de alto padrão **Mari Corretora**, com atuação em Porto Belo e Itapema, Santa Catarina.

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (vanilla) |
| Backend | Python 3.12 + Django 5.1 |
| Database | MySQL 8.4 |
| Servidor WSGI | Gunicorn |
| Proxy reverso | Traefik v3 |
| Container | Docker + Docker Compose |
| Admin UI | Django Jazzmin |

## Estrutura do Projeto

```
mari_corretora/
├── core/                       # App principal
│   ├── models.py               # SiteConfig, CarouselImage, Property, PropertyImage, Testimonial
│   ├── admin.py                # Admin personalizado com image previews
│   ├── views.py                # View da home
│   ├── urls.py                 # Rotas do app
│   ├── templates/core/         # Templates HTML
│   ├── static/core/            # CSS, JS, imagens estáticas
│   └── management/commands/    # Comandos personalizados (seed_data)
├── imoveis/                    # App reservado para expansão futura
├── mari_corretora/             # Settings, URLs raiz, WSGI
├── manage.py
├── Dockerfile
└── requirements.txt
```

## Como Rodar

### Pré-requisitos

- Docker 24+ e Docker Compose v2+
- Portas 80 e 443 livres (ou ajuste no `.env`)
- Domínios configurados no `/etc/hosts` para ambiente local:
  ```
  127.0.0.1 mari.localhost www.mari.localhost
  ```

### Subindo o ambiente

```bash
# Build e start
docker compose up -d --build

# Criar superusuário admin
docker compose exec django python manage.py createsuperuser

# Popular dados iniciais
docker compose exec django python manage.py seed_data

# Coletar estáticos
docker compose exec django python manage.py collectstatic --noinput
```

### Acessos

| Serviço | URL |
|---|---|
| Landing page | http://mari.localhost |
| Admin | http://mari.localhost/admin |
| Traefik Dashboard | http://traefik.mari.localhost |
| MySQL | localhost:3307 |

## Funcionalidades Implementadas

### Landing Page

- **Top Bar**: faixa fixa navy com contato (WhatsApp, email) e borda dourada
- **Header**: logotipo (SVG provisório ou upload via admin), menu de navegação (Home, Imóveis, Sobre, Contato), efeito de scroll, versão mobile com hamburger
- **Hero Section**: slideshow de background, badge "Alto Padrão", título, subtítulo, botão CTA do WhatsApp, indicador de scroll
- **Carrossel de Imóveis**: 6 empreendimentos icônicos da região com transição automática, navegação por dots e setas, suporte a touch, pausa no hover
- **Imóveis em Destaque**: cards responsivos com foto, badge de tipo (Luxo/Cobertura), características, preço e botão "Saiba Mais"
- **Seção "Por que investir aqui"**: texto institucional com estatísticas animadas via Intersection Observer (valorização, praias, retorno)
- **Depoimentos**: cards com avaliação por estrelas, avatar com fallbar (iniciais), nome e texto
- **CTA final**: box destacado com fundo navy/gradiente e link direto ao WhatsApp
- **Footer**: logotipo, navegação, contato (WhatsApp, telefone, email, endereço), redes sociais, região de atuação
- **WhatsApp flutuante**: botão fixo no canto inferior direito com animação pulse
- **Scroll to top**: botão visível após 500px de scroll
- **Preloader**: animação de entrada com logo e linha progressiva

### Painel Admin (Jazzmin)

- Tema escuro navy com acentos dourados
- **Imóveis**: cadastro completo com inline de fotos, preview das imagens, busca, filtros
- **Carrossel**: ordenação drag-and-drop, preview, ativar/desativar
- **Depoimentos**: foto com preview circular, avaliação por estrelas (1-5)
- **Configurações**: formulário simplificado (sem abas, sem customização extra), campos em ordem direta

### Modelos de Dados

```python
SiteConfig       # Configurações globais (logo, contato, hero, redes sociais)
CarouselImage    # Imagens do carrossel (título, legenda, ordem)
Property         # Imóvel (título, slug, descrição, tipo, endereço, preço, área, destaque)
PropertyImage    # Fotos do imóvel (inline, múltiplas, ordenação)
Testimonial      # Depoimento (nome, foto, texto, rating)
```

### Design System

- **Paleta**: navy (`#0f1a2e`, `#1a2744`), gold (`#c8a84e`, `#dfc274`), white, off-white
- **Tipografia**: Cormorant Garamond (serifada, títulos) + Montserrat (sans-serif, corpo)
- **Responsivo**: breakpoints em 1024px, 768px, 480px
- **Animações**: transições suaves em cards, hover de imagens, parallax sutil no hero, contadores animados

## Administração de Conteúdo

### 1. Configurações do Site

Acessar `/admin/core/siteconfig/` para alterar:
- Logotipo da marca
- Número do WhatsApp, telefone e email
- Endereço
- Links das redes sociais (Instagram, Facebook, YouTube, LinkedIn)
- Textos do Hero (título, subtítulo, texto do botão)
- Texto da seção "Sobre / Por que investir"

### 2. Carrossel de Imagens

Acessar `/admin/core/carouselimage/`:
- Fazer upload das imagens (recomendado: 1920x1080px, landscape)
- Definir título e legenda para cada slide
- Ordenar por prioridade
- Ativar/desativar individualmente

### 3. Imóveis

Acessar `/admin/core/property/`:
- Cadastrar título, descrição completa e resumida
- Selecionar tipo (Padrão, Luxo, Cobertura, Comercial, Terreno)
- Preencher endereço, bairro, cidade
- Definir preço, quartos, suítes, banheiros, vagas, área
- Marcar como "Destaque" para aparecer na home
- Adicionar múltiplas fotos (inline), marcar uma como principal

### 4. Depoimentos

Acessar `/admin/core/testimonial/`:
- Nome do cliente
- Foto (opcional, fallback para iniciais)
- Texto do depoimento
- Avaliação de 1 a 5 estrelas
- Ativar/desativar

## Melhorias Futuras

### Prioridade Alta

- [ ] **Página individual de imóvel** (`/imoveis/<slug>`): rota detalhada com galeria completa, planta baixa, vídeo tour, formulário de interesse
- [ ] **Filtro de busca**: por cidade, tipo, preço, quartos, área — com AJAX ou HTMX
- [ ] **SEO**: meta tags dinâmicas, Open Graph, JSON-LD (Schema.org/RealEstateListing), sitemap.xml
- [ ] **Formulário de contato**: formulário funcional com envio de email (SendGrid/Mailgun) e salvamento no banco
- [ ] **Blog/Notícias**: artigos sobre mercado imobiliário, dicas de investimento, lançamentos

### Prioridade Média

- [ ] **Galeria de vídeos**: upload e preview de vídeos dos imóveis (YouTube embed + arquivo local)
- [ ] **Dark mode**: toggle claro/escuro respeitando preferência do sistema
- [ ] **Comparador de imóveis**: selecionar até 3 imóveis e comparar lado a lado
- [ ] **Cache**: implementar Redis para cache de páginas e queries pesadas
- [ ] **i18n**: suporte a inglês/espanhol
- [ ] **WhatsApp API**: pré-preenchimento de mensagem com link do imóvel
- [ ] **Notificações**: alerta de novos imóveis via email/WhatsApp para leads cadastrados

### Prioridade Baixa

- [ ] **Tour virtual 360°**: integração com Matterport ou similar
- [ ] **Calculadora de financiamento**: simulação com parcelas baseadas no preço
- [ ] **Mapa interativo**: imóveis geolocalizados no mapa da região
- [ ] **Área do cliente**: login para favoritar imóveis e agendar visitas
- [ ] **Performance**: lazy loading nativo, compressão de imagens (WebP automático), CDN
- [ ] **PWA**: suporte a instalável, service worker e cache offline

## Manutenção

### Backup

```bash
# Backup do banco
docker compose exec db mysqldump -u mari_user -pmari_pass_2026 mari_corretora > backup_$(date +%Y%m%d).sql

# Restore
cat backup.sql | docker compose exec -T db mysql -u mari_user -pmari_pass_2026 mari_corretora
```

### Migrations

```bash
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate
```

### Logs

```bash
docker compose logs -f django
docker compose logs -f db
docker compose logs -f traefik
```

### Atualizar dependências

```bash
docker compose exec django pip install novo-pacote
# Atualizar requirements.txt
docker compose exec django pip freeze > requirements.txt
```

## Variáveis de Ambiente (`.env`)

```
SECRET_KEY=           # Chave secreta do Django (gerar com: openssl rand -hex 32)
DEBUG=                # True para desenvolvimento, False em produção
ALLOWED_HOSTS=        # Hosts permitidos separados por vírgula
DB_NAME=              # Nome do banco MySQL
DB_USER=              # Usuário do banco
DB_PASSWORD=          # Senha do banco
DB_HOST=              # Host do banco (db no Docker)
DB_PORT=              # Porta do banco (3306)
```

## Changelog

### 2026-06-04

- **Logo provisório**: SVG inline com texto "MARI" dourado + "CORRETORA" branco (`core/static/core/images/logo.svg`); usado como fallback quando não há upload no admin
- **Top bar**: faixa fixa navy escuro acima do header com WhatsApp e email, borda dourada sutil
- **Admin simplificado**: `SiteConfigAdmin` reduzido a `list_display` apenas (sem `fields`, `fieldsets`, custom CSS, `logo_preview`)
- **Jazzmin Customizer removido**: `show_ui_builder: false` no `JAZZMIN_SETTINGS` desabilita o painel "Customize" lateral
- **STORAGES corrigido**: chave `"default"` adicionada com `django.core.files.storage.FileSystemStorage` para uploads funcionarem
- **Seed data reparado**: sintaxe corrigida no `seed_data.py` (fechamento de parênteses)

### Anteriores

- Setup inicial com Django 5.1, MySQL 8.4, Traefik v3, Jazzmin
- Modelos: SiteConfig, CarouselImage, Property, PropertyImage, Testimonial
- Landing page completa com hero, carrossel, imóveis, depoimentos, CTA, footer
- Design system navy/gold/white com tipografia Cormorant Garamond + Montserrat
- Admin com previews de imagem, inlines, busca e filtros

## Licença

Proprietário — Mari Corretora
