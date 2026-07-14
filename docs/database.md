# JP Marketplace Monitor

## Database Architecture v2.1

---

# Objetivo

O banco deve suportar:

- múltiplos usuários
- múltiplos marketplaces
- múltiplas categorias
- múltiplas pesquisas
- múltiplas palavras-chave
- histórico de preços
- notificações
- futuras integrações (Web, API, IA)

---

# Entidades

User

↓

Search

↓

Keywords

↓

Negative Keywords

↓

Listings

↓

Price History

↓

Notifications

---

# User

Representa um usuário do sistema.

Campos

id

telegram_id

username

created_at

updated_at

---

# Search

Representa uma pesquisa criada pelo usuário.

Exemplo:

Omega De Ville Tank

Nikon FM2

Dupont Ligne 2

Campos

id

internal_code

user_id

name

category

marketplace

max_price

active

created_at

updated_at

Uma Search possui:

- várias Keywords

- várias NegativeKeywords

- vários Listings

---

# Keyword

Representa uma palavra de busca.

Exemplo

オメガ デビル

Omega De Ville

511.0410

Campos

id

search_id

keyword

created_at

---

# NegativeKeyword

Palavras proibidas.

Exemplo

ジャンク

部品

まとめ売り

Campos

id

search_id

keyword

created_at

---

# Listing

Representa um anúncio encontrado.

IMPORTANTE

Um Listing é único.

Ele NÃO pertence exclusivamente a uma Search.

Campos

id

marketplace

external_id

url

title

translated_title

category

brand

model

reference

condition

seller

price

currency

image_url

auction_end

created_at

last_seen

---

# SearchListing

Tabela de relacionamento.

Permite que um anúncio pertença a várias pesquisas.

Campos

search_id

listing_id

matched_keyword

created_at

---

# PriceHistory

Histórico de preços.

Campos

id

listing_id

price

recorded_at

---

# Notification

Controle de notificações.

Campos

id

user_id

listing_id

type

sent_at

---

# Alias

Tabela preparada para IA.

Exemplo

Categoria

watch

Marca

Omega

Modelo

De Ville

Aliases

オメガ デビル

Omega De Ville

デヴィル

Campos

id

category

brand

model

alias

created_at

---

# Categorias

watch

camera

pen

lighter

other

---

# Marketplaces

Yahoo Auctions

Mercari

Rakuma

Yahoo Shopping

---

# Filosofia

Search representa um objetivo.

Keyword representa uma estratégia de busca.

Listing representa um anúncio.

Um anúncio pode atender várias pesquisas.

Nunca duplicar Listings.

Todo histórico deve ser preservado.

Nenhuma informação deve ser perdida.

