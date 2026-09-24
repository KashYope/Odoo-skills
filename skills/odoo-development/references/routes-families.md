# Cartographie des principales routes Odoo 19

## Mode d’emploi

1. Chercher par besoin, modèle, méthode ou URL dans `routes.jsonl` avec `scripts/query_routes.py`.
2. Lire la fiche ci-dessous puis le handler complet et ses helpers.
3. Vérifier les modules installés et les overrides. Les champs du JSONL sont **déclarés**, jamais présentés comme routage effectif.
4. Préférer service orm, action ou méthode métier si la route n’est qu’un transport interne.
5. Tester le cas autorisé ET un cas interdit avant réutilisation.

## Defaults et pièges

- Source : `odoo/http.py`, `route`, `_generate_routing_rules`, `HttpDispatcher`, `JsonRPCDispatcher`, dispatcher JSON-2.
- Sans override, type HTTP et auth user sont les defaults du framework; un override `@route()` hérite du parent.
- `methods` omis = pas de restriction de verbes au niveau du décorateur; ce n’est pas « GET seulement ». Le handler/dispatcher impose parfois d’autres contraintes.
- CSRF HTTP activé par défaut, validation sur méthodes non sûres; JSON-RPC désactivé par défaut. Pour JSON-2, lire le dispatcher et l’authentification; ne pas transposer le contrat HTTP.
- `auth=none` n’implique pas que l’opération métier n’a pas d’authentification; `auth=public` n’implique pas que les records soient publics.
- JSON-2 porte `type=json2` dans le code natif, distinct de `jsonrpc`; ce n’est pas une invitation à créer des contrôleurs génériques JSON-2 custom.
- Les appels backend et modèles du JSONL sont des indices lexicaux. Ils ne reconstituent pas un graphe d’appels ou une preuve de sécurité.
- Les routes de modules de test sont identifiées séparément; elles ne constituent pas un catalogue de fonctionnalités de production.

## Index des familles

| Besoin | Première piste | Extension préférée |
|---|---|---|
| Login/reset/signup | web, auth_signup | Configuration puis contrôleur hérité |
| Session/utilisateur | web/session, portail/adresse, res.users | Flux natif, modèle, jamais authentification réécrite |
| CRUD/appel modèle | /web/dataset/call_kw | Service orm puis méthode modèle |
| Fichier/image/pièce jointe | /web/content, /web/image, mail/attachment | Flux/widget natif |
| Portail | /my, /my/orders, compteurs | CustomerPortal et template |
| Website/ecommerce | website, website_sale/cart | Page, snippet, template, hook métier |
| Mail/notifications | mail/thread, message/post, bus | mail.thread, activités, service bus |
| Rapport/import/export/action | report, web/export, base_import, web/action | Action/assistant natif |
| API externe | /json/2/<model>/<method> en 19 | Méthode publique sécurisée |
| Administration base | web/database | Administration seulement |
| Autres domaines | Paiements, POS, RH, surveys, événements, localisation | Lire le module propriétaire dans l’index complet |

## Fiches vérifiées

### Authentification web

- **Module / contrôleur** : `web` · `Home.web_login`.
- **Source** : [addons/web/controllers/home.py:103](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/home.py#L103).
- **Routes déclarées** : `/web/login`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `none`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, redirect=None, **kw`.
- **Réponse** : HTML login ou redirection.
- **Sécurité** : Filtre de base, session, credential; CSRF HTTP pour POST; MFA via mécanisme natif.
- **Backend / modèles** : res.users / Session.authenticate.
- **Réutilisation / extension** : Réutiliser /web/login; extension Home et @route(), jamais copie authentification.

### Inscription utilisateur

- **Module / contrôleur** : `auth_signup` · `AuthSignupHome.web_auth_signup`.
- **Source** : [addons/auth_signup/controllers/main.py:39](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/auth_signup/controllers/main.py#L39).
- **Routes déclarées** : `/web/signup`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, *args, **kw`.
- **Réponse** : HTML/redirect.
- **Sécurité** : Activation signup ou token, captcha; valeurs allowlist, validation mots de passe.
- **Backend / modèles** : res.users.signup; helpers signup.
- **Réutilisation / extension** : Configurer avant d’étendre _prepare_signup_values.

### Réinitialisation utilisateur

- **Module / contrôleur** : `auth_signup` · `AuthSignupHome.web_auth_reset_password`.
- **Source** : [addons/auth_signup/controllers/main.py:87](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/auth_signup/controllers/main.py#L87).
- **Routes déclarées** : `/web/reset_password`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, *args, **kw`.
- **Réponse** : HTML/redirect.
- **Sécurité** : Fonction activée ou token; captcha; traitement contrôlé.
- **Backend / modèles** : res.users.reset_password / signup.
- **Réutilisation / extension** : Réutiliser formulaire natif; ne pas créer un reset maison.

### Session web

- **Module / contrôleur** : `web` · `Session.authenticate`.
- **Source** : [addons/web/controllers/session.py:31](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/session.py#L31).
- **Routes déclarées** : `/web/session/authenticate`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `none`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, db, login, password, base_location=None`.
- **Réponse** : Objet session_info JSON-RPC.
- **Sécurité** : db_filter; credential; authentification/MFA; auth none ne signifie pas réussite sans identifiants.
- **Backend / modèles** : Session.authenticate(env, credential); ir.http.session_info.
- **Réutilisation / extension** : Client web/mobile historique; intégration externe : étudier API adaptée.

### Informations session

- **Module / contrôleur** : `web` · `Session.get_session_info`.
- **Source** : [addons/web/controllers/session.py:25](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/session.py#L25).
- **Routes déclarées** : `/web/session/get_session_info`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self`.
- **Réponse** : Objet JSON-RPC.
- **Sécurité** : Utilisateur authentifié; session courante.
- **Backend / modèles** : ir.http.session_info.
- **Réutilisation / extension** : Préférer service utilisateur/session; garder payload interne.

### Chargement client

- **Module / contrôleur** : `web` · `Home.web_client`.
- **Source** : [addons/web/controllers/home.py:46](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/home.py#L46).
- **Routes déclarées** : `/web; /odoo; /odoo/<path:subpath>; /scoped_app/<path:subpath>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `none`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, s_action=None, **kw`.
- **Réponse** : HTML bootstrap ou redirection.
- **Sécurité** : Session et vérifications dans handler malgré auth none.
- **Backend / modèles** : ir.http et res.users.
- **Réutilisation / extension** : Action/menu/vue plutôt que client alternatif.

### Menus

- **Module / contrôleur** : `web` · `Home.web_load_menus`.
- **Source** : [addons/web/controllers/home.py:85](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/home.py#L85).
- **Routes déclarées** : `/web/webclient/load_menus`.
- **Type / méthodes / auth** : `http` / `['GET']` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, lang=None`.
- **Réponse** : Réponse HTTP JSON.
- **Sécurité** : Session user; chargement sous droits; groupes/menu.
- **Backend / modèles** : ir.ui.menu.
- **Réutilisation / extension** : Réutiliser service/menu; pas de menu JSON maison.

### Opération modèle

- **Module / contrôleur** : `web` · `DataSet.call_kw`.
- **Source** : [addons/web/controllers/dataset.py:28](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L28).
- **Routes déclarées** : `/web/dataset/call_kw; /web/dataset/call_kw/<path:path>`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, model, method, args, kwargs, path=None`.
- **Réponse** : Résultat JSON-RPC sérialisable.
- **Sécurité** : auth user; call_kw/get_public_method; droits ORM; valider invariants dans méthodes publiques.
- **Backend / modèles** : Modèle et méthode dynamiques; odoo.service.model.call_kw.
- **Réutilisation / extension** : Service orm; étendre modèle au lieu de route.

### Bouton métier

- **Module / contrôleur** : `web` · `DataSet.call_button`.
- **Source** : [addons/web/controllers/dataset.py:34](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L34).
- **Routes déclarées** : `/web/dataset/call_button; /web/dataset/call_button/<path:path>`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, model, method, args, kwargs, path=None`.
- **Réponse** : Action normalisée ou false.
- **Sécurité** : Mêmes droits que call_kw; aucune sécurité déduite du bouton visible.
- **Backend / modèles** : call_kw puis clean_action.
- **Réutilisation / extension** : Méthode modèle/action; conserver retour.

### Télécharger fichier

- **Module / contrôleur** : `web` · `Binary.content_common`.
- **Source** : [addons/web/controllers/binary.py:62](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L62).
- **Routes déclarées** : `/web/content; /web/content/<string:xmlid>; /web/content/<string:xmlid>/<string:filename>; /web/content/<int:id>; /web/content/<int:id>/<string:filename>; /web/content/<string:model>/<int:id>/<string:field>; /web/content/<string:model>/<int:id>/<string:field>/<string:filename>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, xmlid=None, model='ir.attachment', id=None, field='raw', filename=None, filename_field='name', mimetype=None, unique=False, download=False, access_token=None, nocache=False`.
- **Réponse** : Flux binaire avec en-têtes.
- **Sécurité** : ir.binary._find_record valide objet/jeton; droits sur champ; ne pas faire sudo soi-même.
- **Backend / modèles** : ir.binary._find_record, _get_stream_from; ir.attachment ou modèle/field.
- **Réutilisation / extension** : Réutiliser /web/content et paramètres après test accès.

### Image redimensionnée

- **Module / contrôleur** : `web` · `Binary.content_image`.
- **Source** : [addons/web/controllers/binary.py:165](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L165).
- **Routes déclarées** : `/web/image; /web/image/<string:xmlid>; /web/image/<string:xmlid>/<string:filename>; /web/image/<string:xmlid>/<int:width>x<int:height>; /web/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>; /web/image/<string:model>/<int:id>/<string:field>; /web/image/<string:model>/<int:id>/<string:field>/<string:filename>; /web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>; /web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>; /web/image/<int:id>; /web/image/<int:id>/<string:filename>; /web/image/<int:id>/<int:width>x<int:height>; /web/image/<int:id>/<int:width>x<int:height>/<string:filename>; /web/image/<int:id>-<string:unique>; /web/image/<int:id>-<string:unique>/<string:filename>; /web/image/<int:id>-<string:unique>/<int:width>x<int:height>; /web/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, xmlid=None, model='ir.attachment', id=None, field='raw', filename_field='name', filename=None, mimetype=None, unique=False, download=False, width=0, height=0, crop=False, access_token=None, nocache=False`.
- **Réponse** : Image/flux HTTP.
- **Sécurité** : Résolution native objet, champ, jeton et contrôles image.
- **Backend / modèles** : ir.binary; ir.attachment ou modèle/field.
- **Réutilisation / extension** : Réutiliser /web/image; ne pas créer service de thumbnails.

### Upload backend

- **Module / contrôleur** : `web` · `Binary.upload_attachment`.
- **Source** : [addons/web/controllers/binary.py:219](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L219).
- **Routes déclarées** : `/web/binary/upload_attachment`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, model, id, ufile, callback=None`.
- **Réponse** : Réponse HTTP liée à upload, inspecter corps exact.
- **Sécurité** : Session user; création attachment sous droits; paramètres model/id contrôlés par ORM.
- **Backend / modèles** : ir.attachment.create.
- **Réutilisation / extension** : Réutiliser widget/upload standard; vérifier contrat navigateur.

### Accueil portail

- **Module / contrôleur** : `portal` · `CustomerPortal.home`.
- **Source** : [addons/portal/controllers/portal.py:184](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L184).
- **Routes déclarées** : `/my; /my/home`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, **kw`.
- **Réponse** : HTML QWeb.
- **Sécurité** : auth user; compteurs/domaines limités dans extensions.
- **Backend / modèles** : CustomerPortal._prepare_portal_layout_values; res.users/partner.
- **Réutilisation / extension** : Étendre _prepare_home_portal_values et templates.

### Compteurs portail

- **Module / contrôleur** : `portal` · `CustomerPortal.counters`.
- **Source** : [addons/portal/controllers/portal.py:175](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L175).
- **Routes déclarées** : `/my/counters`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, counters, **kw`.
- **Réponse** : Objet JSON-RPC.
- **Sécurité** : Utilisateur; implémentations doivent appliquer mêmes domaines/droits que listes.
- **Backend / modèles** : _prepare_home_portal_values; modèles des addons.
- **Réutilisation / extension** : Réutiliser compteur conditionnel par clé demandée.

### Modification adresse utilisateur

- **Module / contrôleur** : `portal` · `CustomerPortal.portal_address_submit`.
- **Source** : [addons/portal/controllers/portal.py:465](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L465).
- **Routes déclarées** : `/my/address/submit`.
- **Type / méthodes / auth** : `http` / `['POST']` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, partner_id=None, **form_data`.
- **Réponse** : Réponse HTTP du formulaire; lire retour exact.
- **Sécurité** : POST+CSRF; partenaire éditable par client; validation champs.
- **Backend / modèles** : res.partner; helpers validation/adresse.
- **Réutilisation / extension** : Étendre valeurs autorisées; ne pas exposer write générique public.

### Document vente portail

- **Module / contrôleur** : `sale` · `CustomerPortal.portal_order_page`.
- **Source** : [addons/sale/controllers/portal.py:125](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/controllers/portal.py#L125).
- **Routes déclarées** : `/my/orders/<int:order_id>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, order_id, report_type=None, access_token=None, message=False, download=False, payment_amount=None, amount_selection=None, **kw`.
- **Réponse** : HTML ou rapport selon paramètres.
- **Sécurité** : _document_check_access avec droits ou access_token; token limité au document.
- **Backend / modèles** : sale.order; CustomerPortal helpers.
- **Réutilisation / extension** : Réutiliser /my/orders; extension QWeb et préparation valeurs.

### Accueil website

- **Module / contrôleur** : `website` · `Website.index`.
- **Source** : [addons/website/controllers/main.py:89](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/controllers/main.py#L89).
- **Routes déclarées** : `/`.
- **Type / méthodes / auth** : `omis — défaut/héritage` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, **kw`.
- **Réponse** : HTML/redirect.
- **Sécurité** : Publication, site/langue et contexte; vérifier parents.
- **Backend / modèles** : website et ir.ui.view.
- **Réutilisation / extension** : Page native/template avant nouveau contrôleur.

### Catalogue ecommerce

- **Module / contrôleur** : `website_sale` · `WebsiteSale.shop`.
- **Source** : [addons/website_sale/controllers/main.py:270](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/main.py#L270).
- **Routes déclarées** : `[SHOP_PATH, f'{SHOP_PATH}/page/<int:page>', f'{SHOP_PATH}/category/<model("product.public.category"):category>', f'{SHOP_PATH}/category/<model("product.public.category"):category>/page/<int:page>']`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, page=0, category=None, search='', min_price=0.0, max_price=0.0, tags='', **post`.
- **Réponse** : HTML QWeb.
- **Sécurité** : Produits vendables/publiés, website, prix et filtres; convertisseurs avec erreurs contrôlées.
- **Backend / modèles** : product.template, product.public.category, website.
- **Réutilisation / extension** : _get_additional_shop_values / hooks recherche; pas de copie shop.

### Fiche produit

- **Module / contrôleur** : `website_sale` · `WebsiteSale.product`.
- **Source** : [addons/website_sale/controllers/main.py:548](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/main.py#L548).
- **Routes déclarées** : `[f'{SHOP_PATH}/<model("product.template"):product>', f'{SHOP_PATH}/<model("product.public.category"):category>/<model("product.template"):product>']`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, product, category=None, pricelist=None, **kwargs`.
- **Réponse** : HTML QWeb.
- **Sécurité** : Produit accessible/publié et website; convertisseur modèle.
- **Backend / modèles** : product.template; _prepare_product_values.
- **Réutilisation / extension** : Hériter template ou hook valeurs; route dynamique SHOP_PATH à lire.

### Ajouter au panier

- **Module / contrôleur** : `website_sale` · `Cart.add_to_cart`.
- **Source** : [addons/website_sale/controllers/cart.py:75](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/cart.py#L75).
- **Routes déclarées** : `/shop/cart/add`.
- **Type / méthodes / auth** : `jsonrpc` / `['POST']` / `public`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, product_template_id, product_id, quantity=1.0, uom_id=None, product_custom_attribute_values=None, no_variant_attribute_value_ids=None, linked_products=None, **kwargs`.
- **Réponse** : Objet JSON-RPC.
- **Sécurité** : Commande de session, produit/combinaison/quantité validés par flux natif.
- **Backend / modèles** : sale.order panier et méthodes _cart_*.
- **Réutilisation / extension** : Réutiliser service panier; conserver validations métier.

### Modifier panier

- **Module / contrôleur** : `website_sale` · `Cart.update_cart`.
- **Source** : [addons/website_sale/controllers/cart.py:309](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/cart.py#L309).
- **Routes déclarées** : `/shop/cart/update`.
- **Type / méthodes / auth** : `jsonrpc` / `['POST']` / `public`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, line_id, quantity, product_id=None, **kwargs`.
- **Réponse** : Objet JSON-RPC.
- **Sécurité** : Commande de session et ligne; ne pas accepter une commande arbitraire.
- **Backend / modèles** : sale.order; _cart_*.
- **Réutilisation / extension** : Route native; vérifier signature 19, différente des anciens exemples.

### Transaction paiement

- **Module / contrôleur** : `website_sale` · `PaymentPortal.shop_payment_transaction`.
- **Source** : [addons/website_sale/controllers/payment.py:25](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/payment.py#L25).
- **Routes déclarées** : `/shop/payment/transaction/<int:order_id>`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `public`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, order_id, access_token, **kwargs`.
- **Réponse** : Objet JSON-RPC de traitement.
- **Sécurité** : Vérification commande/token, montant et fournisseur; lire helpers PaymentPortal.
- **Backend / modèles** : sale.order; payment.transaction.
- **Réutilisation / extension** : Réutiliser provider/flux; ne pas confirmer une commande depuis le navigateur.

### Lecture conversation

- **Module / contrôleur** : `mail` · `ThreadController.mail_thread_messages`.
- **Source** : [addons/mail/controllers/thread.py:61](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/controllers/thread.py#L61).
- **Routes déclarées** : `/mail/thread/messages`.
- **Type / méthodes / auth** : `jsonrpc` / `['POST']` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, thread_model, thread_id, fetch_params=None`.
- **Réponse** : Payload JSON-RPC mail.
- **Sécurité** : _get_thread_with_access mode read avant _message_fetch.
- **Backend / modèles** : mail.message et thread_model dynamique.
- **Réutilisation / extension** : Utiliser chatter natif; payload store interne.

### Publication message

- **Module / contrôleur** : `mail` · `ThreadController.mail_message_post`.
- **Source** : [addons/mail/controllers/thread.py:209](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/controllers/thread.py#L209).
- **Routes déclarées** : `/mail/message/post`.
- **Type / méthodes / auth** : `jsonrpc` / `['POST']` / `public`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, thread_model, thread_id, post_data, context=None, **kwargs`.
- **Réponse** : store_data + message_id JSON-RPC.
- **Sécurité** : add_guest_to_context; accès thread pour post; allowlist post_data; sudo seulement après contrôles.
- **Backend / modèles** : thread.message_post; mail.thread/mail.message.
- **Réutilisation / extension** : Préférer message_post côté modèle; préserver contrat invité.

### Pièce jointe chatter

- **Module / contrôleur** : `mail` · `AttachmentController.mail_attachment_upload`.
- **Source** : [addons/mail/controllers/attachment.py:49](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/controllers/attachment.py#L49).
- **Routes déclarées** : `/mail/attachment/upload`.
- **Type / méthodes / auth** : `http` / `['POST']` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, ufile, thread_id, thread_model, is_pending=False, **kwargs`.
- **Réponse** : Réponse HTTP JSON.
- **Sécurité** : Invité/session et accès thread; validation fichier/objet; POST et CSRF natif.
- **Backend / modèles** : ir.attachment; ThreadController helpers.
- **Réutilisation / extension** : Widget pièce jointe natif; ne pas reproduire son sudo hors contexte.

### Notifications temps réel

- **Module / contrôleur** : `bus` · `WebsocketController.websocket`.
- **Source** : [addons/bus/controllers/websocket.py:11](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/bus/controllers/websocket.py#L11).
- **Routes déclarées** : `/websocket`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, version=None`.
- **Réponse** : Handshake websocket.
- **Sécurité** : Auth public seulement au transport; souscriptions et channels contrôlés ailleurs.
- **Backend / modèles** : WebsocketConnectionHandler.open_connection.
- **Réutilisation / extension** : Service bus natif; éviter socket/protocole custom.

### Poll de notifications

- **Module / contrôleur** : `bus` · `WebsocketController.peek_notifications`.
- **Source** : [addons/bus/controllers/websocket.py:31](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/bus/controllers/websocket.py#L31).
- **Routes déclarées** : `/websocket/peek_notifications`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `public`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, channels, last, is_first_poll=False`.
- **Réponse** : Objet channels/notifications.
- **Sécurité** : Session websocket et ir.websocket._prepare_subscribe_data; scope channels/base.
- **Backend / modèles** : ir.websocket; bus.bus._poll.
- **Réutilisation / extension** : Fallback/service natif; pas API publique garantie.

### Rapport HTML/PDF/texte

- **Module / contrôleur** : `web` · `ReportController.report_routes`.
- **Source** : [addons/web/controllers/report.py:23](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/report.py#L23).
- **Routes déclarées** : `/report/<converter>/<reportname>; /report/<converter>/<reportname>/<docids>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, reportname, docids=None, converter=None, **data`.
- **Réponse** : HTTP html/pdf/text selon converter.
- **Sécurité** : Session user puis pipeline rapport et droits sur records; vérifier rapport particulier.
- **Backend / modèles** : ir.actions.report._render_qweb_html/pdf/text.
- **Réutilisation / extension** : report_action et template hérité plutôt que nouvelle route.

### Image code-barres

- **Module / contrôleur** : `web` · `ReportController.report_barcode`.
- **Source** : [addons/web/controllers/report.py:55](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/report.py#L55).
- **Routes déclarées** : `/report/barcode; /report/barcode/<barcode_type>/<path:value>`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `public`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, barcode_type, value, **kwargs`.
- **Réponse** : PNG.
- **Sécurité** : Données/format validés; contenu fourni par appelant.
- **Backend / modèles** : ir.actions.report.barcode.
- **Réutilisation / extension** : Réutiliser en QWeb; ne pas ajouter générateur.

### Export CSV

- **Module / contrôleur** : `web` · `CSVExport.web_export_csv`.
- **Source** : [addons/web/controllers/export.py:640](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/export.py#L640).
- **Routes déclarées** : `/web/export/csv`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, data`.
- **Réponse** : HTTP text/csv téléchargement.
- **Sécurité** : Utilisateur courant; ORM export_data; droit export et champs selon pipeline.
- **Backend / modèles** : ExportFormat.base; modèle dynamique.export_data.
- **Réutilisation / extension** : Export standard; ne pas remplacer par SQL/route.

### Export XLSX

- **Module / contrôleur** : `web` · `ExcelExport.web_export_xlsx`.
- **Source** : [addons/web/controllers/export.py:688](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/export.py#L688).
- **Routes déclarées** : `/web/export/xlsx`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, data`.
- **Réponse** : HTTP fichier XLSX.
- **Sécurité** : Même pipeline et droits export.
- **Backend / modèles** : ExportFormat.base; modèle dynamique.export_data.
- **Réutilisation / extension** : Export standard; adapter format uniquement si besoin absent.

### Upload avant import

- **Module / contrôleur** : `base_import` · `ImportController.set_file`.
- **Source** : [addons/base_import/controllers/main.py:13](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_import/controllers/main.py#L13).
- **Routes déclarées** : `/base_import/set_file`.
- **Type / méthodes / auth** : `omis — défaut/héritage` / `['POST']` / `omis — défaut/héritage`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, id`.
- **Réponse** : HTTP texte JSON {result}.
- **Sécurité** : Décorateur partiel : auth user/type http par défaut pour cette racine; CSRF POST; droits TransientModel.
- **Backend / modèles** : base_import.import.write.
- **Réutilisation / extension** : Ne réalise pas l’import : ensuite execute_import via ORM.

### Chargement action

- **Module / contrôleur** : `web` · `Action.load`.
- **Source** : [addons/web/controllers/action.py:22](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/action.py#L22).
- **Routes déclarées** : `/web/action/load`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, action_id, context=None`.
- **Réponse** : Dictionnaire JSON-RPC.
- **Sécurité** : auth user; métadonnées d’action lues en sudo dans ce handler; cela ne donne aucun droit sur les records métier, contrôlés ensuite.
- **Backend / modèles** : ir.actions.actions puis type spécifique.
- **Réutilisation / extension** : Service action; pas route écran custom.

### Action serveur

- **Module / contrôleur** : `web` · `Action.run`.
- **Source** : [addons/web/controllers/action.py:53](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/action.py#L53).
- **Routes déclarées** : `/web/action/run`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `user`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, action_id, context=None`.
- **Réponse** : Action/résultat JSON-RPC.
- **Sécurité** : auth user; ir.actions.server.run et ses contrôles; ne pas exposer code arbitraire.
- **Backend / modèles** : ir.actions.server.run.
- **Réutilisation / extension** : Configurer petite action ou méthode modèle testable.

### API externe JSON-2

- **Module / contrôleur** : `rpc` · `WebJson2Controller.web_json_2_rpc`.
- **Source** : [addons/rpc/controllers/json2.py:49](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/json2.py#L49).
- **Routes déclarées** : `/json/2/<__model__>/<__method__>`.
- **Type / méthodes / auth** : `json2` / `['POST']` / `bearer`.
- **CSRF** : Dispatcher JSON-2; voir source.
- **Paramètres** : `self, __model__: str, __method__: str, ids: Sequence[int]=(), context: Mapping[str, Any]=frozendict(), **kwargs`.
- **Réponse** : Valeur JSON; recordset converti en IDs; erreurs HTTP.
- **Sécurité** : Bearer/session selon framework; get_public_method; signature.bind; droits ORM; dispatcher json2.
- **Backend / modèles** : Modèle dynamique; méthode publique.
- **Réutilisation / extension** : API externe 19; logique atomique dans une méthode si nécessaire.

### RPC externe historique

- **Module / contrôleur** : `rpc` · `JSONRPC.jsonrpc`.
- **Source** : [addons/rpc/controllers/jsonrpc.py:11](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/jsonrpc.py#L11).
- **Routes déclarées** : `/jsonrpc`.
- **Type / méthodes / auth** : `jsonrpc` / `omises — défaut/héritage` / `none`.
- **CSRF** : JSON-RPC default : inactif, sauf héritage contraire.
- **Paramètres** : `self, service, method, args`.
- **Réponse** : Enveloppe JSON-RPC.
- **Sécurité** : auth none au transport; credentials et ACL au service; déprécié.
- **Backend / modèles** : http.dispatch_rpc services common/db/object.
- **Réutilisation / extension** : Migrer intégration vers JSON-2 lorsque cible compatible.

### XML-RPC externe historique

- **Module / contrôleur** : `rpc` · `XMLRPC.xmlrpc_2`.
- **Source** : [addons/rpc/controllers/xmlrpc.py:156](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/xmlrpc.py#L156).
- **Routes déclarées** : `/xmlrpc/2/<service>`.
- **Type / méthodes / auth** : `omis — défaut/héritage` / `['POST']` / `none`.
- **CSRF** : False.
- **Paramètres** : `self, service`.
- **Réponse** : XML-RPC.
- **Sécurité** : POST, csrf False explicite; credentials service; déprécié.
- **Backend / modèles** : Services common/db/object.
- **Réutilisation / extension** : Ne pas créer une nouvelle intégration durable sans plan de migration.

### Documentation API de l’instance

- **Module / contrôleur** : `api_doc` · `DocController.doc_client`.
- **Source** : [addons/api_doc/controllers/api_doc.py:38](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/api_doc/controllers/api_doc.py#L38).
- **Routes déclarées** : `/doc; /doc/<model_name>; /doc/index.html`.
- **Type / méthodes / auth** : `http` / `omises — défaut/héritage` / `user`.
- **CSRF** : HTTP default : actif pour méthodes non sûres, sauf héritage contraire.
- **Paramètres** : `self, mod=None, **kwargs`.
- **Réponse** : HTML.
- **Sécurité** : auth user et groupe api_doc.group_allow_doc; documentation dynamique liée aux modèles présents.
- **Backend / modèles** : Contrôleur api_doc; modèles installés.
- **Réutilisation / extension** : Vérifier API réellement exposée sur l’instance; pas d’invention de méthodes.

### Administration des bases

- **Module / contrôleur** : `web` · `Database.backup`.
- **Source** : [addons/web/controllers/database.py:126](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/database.py#L126).
- **Routes déclarées** : `/web/database/backup`.
- **Type / méthodes / auth** : `http` / `['POST']` / `none`.
- **CSRF** : False.
- **Paramètres** : `self, master_pwd, name, backup_format='zip', filestore=True`.
- **Réponse** : Flux sauvegarde.
- **Sécurité** : auth none/CSRF False; mot de passe maître et contrôles service; haut privilège.
- **Backend / modèles** : odoo.service.db.
- **Réutilisation / extension** : Ne pas réutiliser pour une fonction utilisateur; outil administration seulement.

