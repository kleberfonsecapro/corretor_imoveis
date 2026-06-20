# Análise de Segurança — Mari Corretora

## Resumo

| Gravidade | Quantidade |
|-----------|-----------|
| **CRÍTICO** | 5 |
| **ALTO** | 7 |
| **MÉDIO** | 12 |
| **BAIXO** | 9 |
| **TOTAL** | 33 |

---

## CRÍTICOS

### 1. SECRET_KEY, credenciais do banco e variáveis de ambiente expostas no Git

**Arquivo:** `.env` (committed nos commits `51bde3a` e `6c3b6a0`)
**Arquivo:** `.gitignore` linha 4 — só ignora `.env` após os commits já terem sido feitos

O `.env` foi commitado e contém:
- `SECRET_KEY=django-insecure-change-this-in-production-abc123xyz`
- `DEBUG=True`
- `DB_PASSWORD=mari_pass_2026`
- `DB_USER=mari_user`
- `DB_NAME=mari_corretora`
- `ALLOWED_HOSTS=localhost,127.0.0.1,mari.localhost`

Mesmo que o `.env` atual esteja no `.gitignore`, o histórico do Git mantém esses dados. Qualquer um com acesso ao repositório pode obter a SECRET_KEY e conectar diretamente no banco.

---

### 2. SECRET_KEY placeholder genérica

**Arquivo:** `mari_corretora/mari_corretora/settings.py:7`
**Arquivo:** `.env` no histórico do Git

A `SECRET_KEY` = `django-insecure-change-this-in-production-abc123xyz` é o placeholder padrão do Django. Compromete assinatura de sessões, tokens CSRF, tokens de reset de senha e qualquer dado assinado pelo Django.

---

### 3. Senha root do MySQL hardcoded no docker-compose.yml

**Arquivo:** `docker-compose.yml:27`

```yaml
MYSQL_ROOT_PASSWORD: root_pass_2026
```

---

### 4. Senha do usuário do banco hardcoded no docker-compose.yml

**Arquivo:** `docker-compose.yml:30`

```yaml
MYSQL_PASSWORD: mari_pass_2026
```

---

### 5. Senha do banco exposta em comandos no README.md

**Arquivo:** `README.md:201,204`

```bash
docker compose exec db mysqldump -u mari_user -pmari_pass_2026 mari_corretora
cat backup.sql | docker compose exec -T db mysql -u mari_user -pmari_pass_2026 mari_corretora
```

---

## ALTOS

### 6. DEBUG=True configurado

**Arquivo:** `.env` no histórico do Git — `DEBUG=True`

Se deployed em produção, Django exibirá páginas de erro com trace completo, variáveis de ambiente (incluindo SECRET_KEY e senhas) e configurações.

---

### 7. Sem HTTPS/TLS

**Arquivo:** `traefik/dynamic.yml:5-6` — usa entrypoint `web` (porta 80) sem `web-secure` (443)

Sem certificado TLS, sem Let's Encrypt, sem redirecionamento HTTPS. Todo o tráfego é texto puro.

**Configurações ausentes em settings.py:**
- `SECURE_SSL_REDIRECT`
- `SECURE_PROXY_SSL_HEADER`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`

---

### 8. CORS permite qualquer origem (`*`)

**Arquivo:** `traefik/dynamic.yml:28-29`

```yaml
accessControlAllowOriginList:
  - "*"
```

Qualquer site pode fazer requisições para o backend Django, incluindo o admin, em nome de usuários autenticados.

---

### 9. Session cookie sem flag Secure

**Arquivo:** `mari_corretora/mari_corretora/settings.py`

`SESSION_COOKIE_SECURE` não configurado (default `False`). Cookies de sessão trafegam em HTTP puro.

---

### 10. CSRF cookie sem flag Secure

**Arquivo:** `mari_corretora/mari_corretora/settings.py`

`CSRF_COOKIE_SECURE` não configurado (default `False`). Tokens CSRF trafegam em HTTP puro.

---

### 11. SECURE_PROXY_SSL_HEADER não configurado atrás de proxy reverso

**Arquivo:** `mari_corretora/mari_corretora/settings.py`

Django roda atrás do Traefik mas não tem `SECURE_PROXY_SSL_HEADER` configurado. Django não consegue determinar se a requisição é HTTPS, quebrando redirects e verificações de segurança.

---

### 12. Senha do banco legível via Docker

**Arquivo:** `docker-compose.yml:38`

A senha do MySQL fica acessível via `docker inspect` e logs do container.

---

## MÉDIOS

### 13. Dashboard do Traefik exposto com autenticação placeholder

**Arquivo:** `traefik/dynamic.yml:11-17,48-51`

```yaml
users:
  - "admin:$2y$10$YourHashedPasswordHere"
```

O hash `$2y$10$YourHashedPasswordHere` não é um hash bcrypt válido para nenhuma senha real. A autenticação pode ser inexistente ou contornável.

---

### 14. Socket Docker montado no container Traefik

**Arquivo:** `traefik/traefik.yml:12-13`

```yaml
endpoint: "unix:///var/run/docker.sock"
```

Se o container Traefik for comprometido, o atacante tem controle total sobre o Docker host.

---

### 15. Sem validação de tamanho de upload

**Arquivos:** `core/models.py:36,109,129` — `ImageField` sem validação de tamanho máximo

**settings.py:** `DATA_UPLOAD_MAX_MEMORY_SIZE` e `FILE_UPLOAD_MAX_MEMORY_SIZE` não configurados. Atacante pode causar DoS por exaustão de disco.

---

### 16. Sem validação de Content-Type em uploads

**Arquivos:** Mesmo que #15

`ImageField` valida que o arquivo é uma imagem válida via Pillow, mas não há validação adicional de magic bytes. Um arquivo poliglota (imagem + código malicioso) pode ser enviado.

---

### 17. Headers de segurança ausentes no Django

**Arquivo:** `mari_corretora/mari_corretora/settings.py`

Ausentes (parcialmente mitigados pelo Traefik):
- `SECURE_CONTENT_TYPE_NOSNIFF`
- `SECURE_BROWSER_XSS_FILTER`
- `SECURE_REFERRER_POLICY`
- `SECURE_HSTS_SECONDS`

---

### 18. Sem Content Security Policy (CSP)

**Arquivo:** `mari_corretora/mari_corretora/settings.py` e `traefik/dynamic.yml`

Nenhum header CSP configurado. As páginas carregam recursos externos (Google Fonts, Font Awesome, Unsplash) sem whitelist.

---

### 19. Sem rate limiting

Nenhum endpoint tem limitação de taxa. O login do admin em `/admin/` é vulnerável a ataques de força bruta.

---

### 20. Admin exposto sem proteções adicionais

**Arquivo:** `mari_corretora/mari_corretora/urls.py:7`

`/admin/` acessível sem:
- IP whitelisting
- Autenticação de dois fatores
- Rate limiting
- Ofuscação de URL

---

### 21. Slug de imóvel sem tratamento de colisão

**Arquivo:** `core/models.py:91-94`

```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
```

Se dois imóveis tiverem títulos que gerem o mesmo slug, o segundo salvo levanta `IntegrityError` (erro 500).

---

### 22. Arquivos de mídia servidos pelo Django em DEBUG

**Arquivo:** `mari_corretora/mari_corretora/urls.py:11-12`

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Se DEBUG estiver ativo em produção, arquivos de mídia são servidos pelo Django. Além disso, não há configuração no Traefik para servir `/media/` em produção.

---

### 23. Porta do MySQL exposta para o host

**Arquivo:** `docker-compose.yml:34`

```yaml
ports:
  - "3307:3306"
```

O banco de dados pode ser acessado diretamente de fora da rede Docker.

---

### 24. CKEditor instalado mas não usado

**Arquivo:** `requirements.txt:8` e `settings.py:168-174`

`django-ckeditor==6.7.2` está instalado e configurado com toolbar "Full", mas nenhum campo do modelo o utiliza. Dependência morta aumenta superfície de ataque.

---

## BAIXOS

### 25. HSTS não configurado

**Arquivo:** `settings.py`

`SECURE_HSTS_SECONDS` não configurado. Usuários podem ser rebaixados para HTTP via MITM quando HTTPS for implementado.

---

### 26. Sessão sem timeout de inatividade

**Arquivo:** `settings.py`

`SESSION_COOKIE_AGE` default de 2 semanas. Sessão do admin persiste mesmo após fechar o navegador (`SESSION_EXPIRE_AT_BROWSER_CLOSE = False`).

---

### 27. Validadores de senha sem personalização

**Arquivo:** `settings.py:71-76`

`MinimumLengthValidator` usa mínimo de 8 caracteres (default). Sem exigência de 12+ caracteres para admin.

---

### 28. Logging mínimo

**Arquivo:** `settings.py:176-188`

Apenas console handler em nível INFO. Sem logging específico de segurança, sem persistência, sem rotação.

---

### 29. App `imoveis` vazio mas registrado

**Arquivo:** `settings.py:21`

App sem models, views ou URLs. Código incompleto aumenta ruído e superfície.

---

### 30. Dados de contato hardcoded

**Arquivos:** `core/templates/core/index.html:30-35`, `core/management/commands/seed_data.py:12-14`

WhatsApp e email fixos no código e templates. Dados pessoais em versionamento.

---

### 31. SECURE_BROWSER_XSS_FILTER ausente no Django

**Arquivo:** `settings.py`

Mitigado parcialmente pelo Traefik, mas não configurado no Django.

---

### 32. SECURE_CONTENT_TYPE_NOSNIFF ausente no Django

**Arquivo:** `settings.py`

Mitigado parcialmente pelo Traefik, mas não configurado no Django.

---

### 33. DATA_UPLOAD_MAX_NUMBER_FIELDS não configurado

**Arquivo:** `settings.py`

Pode permitir DoS via flooding de campos de formulário.

---

## Itens verificados e considerados seguros

| Item | Status | Detalhes |
|------|--------|----------|
| **SQL Injection** | ✅ Seguro | ORM do Django, sem SQL bruto |
| **XSS em Templates** | ✅ Seguro | Auto-escaping do Django ativo; `linebreaks` é seguro |
| **CSRF** | ✅ Seguro | `CsrfViewMiddleware` ativo |
| **Template Injection** | ✅ Seguro | Templates são arquivos fixos, sem input do usuário |
| **Open Redirect** | ✅ Seguro | Sem views de redirect que aceitem URLs do usuário |
| **SSRF** | ✅ Seguro | Nenhuma requisição HTTP externa nas views |
| **IDOR** | ✅ Seguro | Nenhuma view aceita IDs de objetos do usuário |
| **Mass Assignment** | ✅ Seguro | Sem `fields = '__all__'` |
| **Clickjacking** | ✅ Seguro | `XFrameOptionsMiddleware` ativo (default `DENY`) + Traefik `frameDeny: true` |
| **Whitenoise** | ✅ Seguro | Configurado corretamente para servir arquivos estáticos |
