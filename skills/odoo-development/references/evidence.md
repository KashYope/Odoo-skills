# Registre de preuves et méthode

## Périmètre

Les arbres ont été récupérés sans troncature. Les fichiers récupérés sont listés et hachés dans coverage.json; les autres fichiers de l’arbre n’ont pas été lus. La cartographie couvre les fichiers Python controllers hors __init__ de 19, plus le corpus framework/métier sélectionné. Elle ne couvre pas les routes générées dynamiquement hors corpus, les addons tiers ou Enterprise. Les corps téléchargés ne sont pas tous soumis à une analyse humaine équivalente : extraction systématique, puis lecture approfondie des points d’entrée et des 39 fiches.

| Branche | SHA | Fichiers récupérés |
|---|---|---|
| 17.0 | `b4c6b344a7a6cef93db339c56edb4feb5b222435` | 12 |
| 18.0 | `c270965ec11c95e5e2866b30f8fa2c90287c6e8a` | 12 |
| 19.0 | `2e2acfd6d2725d1a4a95b1a6056334e1ac34163f` | 792 |

## Règles structurantes : contrat et usages croisés

### Extension de modèle et batch

- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334)
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34)
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21)

### Delta métier dans hook de préparation

- [`addons/sale/models/sale_order.py` · `SaleOrder._prepare_invoice`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L1413)
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder._prepare_invoice`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L925)

### Mixins plutôt que duplication

- [`addons/mail/models/mail_thread.py` · `MailThread`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_thread.py#L64)
- [`addons/crm/models/crm_lead.py` · `Lead`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/crm/models/crm_lead.py#L1)
- [`addons/project/models/project_project.py` · `ProjectProject`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/models/project_project.py#L23)

### Vue héritée plutôt que copie

- [`odoo/addons/base/models/ir_ui_view.py` · `IrUiView`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_ui_view.py#L139)
- [`addons/sale/views/sale_order_views.xml` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/views/sale_order_views.xml#L1)
- [`addons/purchase/views/purchase_views.xml` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/views/purchase_views.xml#L1)

### Redécoration du contrôleur hérité

- [`odoo/http.py` · `Controller`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L706)
- [`addons/auth_signup/controllers/main.py` · `AuthSignupHome.web_login`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/auth_signup/controllers/main.py#L26)
- [`addons/website/controllers/main.py` · `Website`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/controllers/main.py#L87)

### Contrôle objet même sous auth public

- [`addons/web/controllers/binary.py` · `Binary.content_common`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L72)
- [`addons/portal/controllers/portal.py` · `CustomerPortal._document_check_access`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L961)
- [`addons/mail/controllers/thread.py` · `ThreadController._get_thread_with_access`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/controllers/thread.py#L48)

### ORM/service au lieu de route CRUD

- [`addons/web/static/src/core/orm_service.js` · `ORM`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/orm_service.js#L98)
- [`addons/web/controllers/dataset.py` · `DataSet.call_kw`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L29)
- [`odoo/service/model.py` · `get_public_method`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/service/model.py#L45)

### Séparer progression cron et transactions métier

- [`odoo/addons/base/models/ir_cron.py` · `IrCron._commit_progress`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_cron.py#L846)
- [`odoo/service/model.py` · `retrying`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/service/model.py#L160)

Les règles de minimisation sont une synthèse d’ingénierie dérivée de ces mécanismes; elles ne sont pas présentées comme une citation officielle. Les hooks isolés sont signalés dans extension-points.md.

## Fichiers et symboles vérifiés

| Chemin/module | Symboles observés (sélection) |
|---|---|
| [`addons/auth_signup/controllers/main.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/auth_signup/controllers/main.py#L1) | `AuthSignupHome`; `AuthSignupHome.web_login`; `AuthSignupHome._prepare_signup_values`; `AuthBaseSetup` |
| [`addons/base_automation/models/base_automation.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_automation/models/base_automation.py#L1) | `_get_domain_fields`; `_domain_fields_differences`; `_keep_to_compute`; `get_webhook_request_payload`; `BaseAutomation`; `BaseAutomation.create`; `BaseAutomation.write`; `BaseAutomation._prepare_loggin_values` |
| [`addons/base_import/controllers/main.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_import/controllers/main.py#L1) | `ImportController` |
| [`addons/base_import/models/base_import.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_import/models/base_import.py#L1) | `ImportValidationError`; `Base`; `Base_ImportMapping`; `ResUsers`; `Base_ImportImport`; `Base_ImportImport.execute_import`; `check_patterns`; `to_re`; `_replacer`; `read_file_failed` |
| [`addons/bus/models/bus.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/bus/models/bus.py#L1) | `get_notify_payload_max_length`; `json_dump`; `hashable`; `channel_with_db`; `get_notify_payloads`; `BusBus`; `BusSubscription`; `ImDispatch` |
| [`addons/crm/models/crm_lead.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/crm/models/crm_lead.py#L1) | `CrmLead`; `CrmLead._prepare_values_from_partner`; `CrmLead._prepare_address_values_from_partner`; `CrmLead._prepare_contact_name_from_partner`; `CrmLead._prepare_partner_name_from_partner`; `CrmLead.create`; `CrmLead.write`; `CrmLead._prepare_customer_values` |
| [`addons/mail/models/mail_activity_mixin.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_activity_mixin.py#L1) | `MailActivityMixin`; `MailActivityMixin.activity_schedule` |
| [`addons/mail/models/mail_alias_mixin.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_alias_mixin.py#L1) | `MailAliasMixin` |
| [`addons/mail/models/mail_template.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_template.py#L1) | `MailTemplate`; `MailTemplate.create`; `MailTemplate.write` |
| [`addons/mail/models/mail_thread.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_thread.py#L1) | `MailThread`; `MailThread.create`; `MailThread.write`; `MailThread.message_post` |
| [`addons/portal/controllers/portal.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L1) | `pager`; `get_records_pager`; `_build_url_w_params`; `CustomerPortal`; `CustomerPortal._prepare_portal_layout_values`; `CustomerPortal._prepare_home_portal_values`; `CustomerPortal._prepare_my_account_rendering_values`; `CustomerPortal._prepare_address_data`; `CustomerPortal._prepare_address_form_values`; `CustomerPortal._document_check_access`; `get_error` |
| [`addons/portal/models/portal_mixin.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/models/portal_mixin.py#L1) | `PortalMixin` |
| [`addons/project/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/__manifest__.py#L1) |  |
| [`addons/project/models/project_project.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/models/project_project.py#L1) | `ProjectProject`; `ProjectProject.create`; `ProjectProject.write` |
| [`addons/purchase/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/__manifest__.py#L1) |  |
| [`addons/purchase/controllers/portal.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/controllers/portal.py#L1) | `CustomerPortal`; `CustomerPortal._prepare_home_portal_values` |
| [`addons/purchase/models/purchase_order.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L1) | `PurchaseOrder`; `PurchaseOrder.create`; `PurchaseOrder.message_post`; `PurchaseOrder._prepare_supplier_info`; `PurchaseOrder._prepare_down_payment_section_values`; `PurchaseOrder._prepare_grouped_data`; `PurchaseOrder._prepare_invoice` |
| [`addons/purchase/tests/test_purchase.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/tests/test_purchase.py#L1) | `TestPurchase` |
| [`addons/purchase/views/purchase_views.xml` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/views/purchase_views.xml#L1) | `menu_purchase_root`; `menu_procurement_management`; `menu_procurement_management_supplier_name`; `menu_purchase_config`; `menu_product_pricelist_action2_purchase`; `menu_product_in_config_purchase`; `menu_product_in_config_purchase`; `menu_product_attribute_action` |
| [`addons/rpc/controllers/json2.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/json2.py#L1) | `WebJson2Controller` |
| [`addons/rpc/controllers/jsonrpc.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/jsonrpc.py#L1) | `JSONRPC` |
| [`addons/sale/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/__manifest__.py#L1) |  |
| [`addons/sale/controllers/portal.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/controllers/portal.py#L1) | `CustomerPortal`; `CustomerPortal._prepare_home_portal_values`; `CustomerPortal._prepare_quotations_domain`; `CustomerPortal._prepare_orders_domain`; `CustomerPortal._prepare_sale_portal_rendering_values`; `PaymentPortal` |
| [`addons/sale/models/sale_order.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L1) | `SaleOrder`; `SaleOrder.create`; `SaleOrder.write`; `SaleOrder.action_confirm`; `SaleOrder._prepare_confirmation_values`; `SaleOrder._prepare_invoice`; `SaleOrder.message_post`; `SaleOrder._prepare_analytic_account_data`; `SaleOrder._prepare_down_payment_section_line`; `SaleOrder._prepare_down_payment_line_section_values`; `SaleOrder._prepare_down_payment_line_values_from_base_line` |
| [`addons/sale/security/ir.model.access.csv` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/security/ir.model.access.csv#L1) |  |
| [`addons/sale/tests/test_sale_order.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/tests/test_sale_order.py#L1) | `TestSaleOrder`; `TestSaleOrderInvoicing`; `TestSalesTeam`; `TestSaleMailComposerUI` |
| [`addons/sale/views/sale_order_views.xml` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/views/sale_order_views.xml#L1) | `sale_order_view_activity`; `view_sale_order_calendar`; `view_sale_order_graph`; `view_sale_order_pivot`; `view_sale_order_kanban`; `sale_order_kanban_upload`; `sale_order_tree`; `view_order_tree` |
| [`addons/stock/models/stock_move.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/stock/models/stock_move.py#L1) | `StockMove`; `StockMove.create`; `StockMove.write`; `StockMove._prepare_merge_moves_distinct_fields`; `StockMove._prepare_merge_negative_moves_excluded_distinct_fields`; `StockMove._prepare_procurement_origin`; `StockMove._prepare_procurement_qty`; `StockMove._prepare_procurement_values`; `StockMove._prepare_move_line_vals`; `StockMove._prepare_move_split_vals` |
| [`addons/web/controllers/action.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/action.py#L1) | `MissingActionError`; `Action` |
| [`addons/web/controllers/binary.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L1) | `clean`; `Binary` |
| [`addons/web/controllers/dataset.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L1) | `DataSet`; `DataSet.call_kw` |
| [`addons/web/controllers/export.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/export.py#L1) | `none_values_filtered`; `allow_empty_iterable`; `GroupsTreeNode`; `ExportXlsxWriter`; `ExportXlsxWriter.write`; `GroupExportXlsxWriter`; `Export`; `ExportFormat`; `CSVExport`; `ExcelExport` |
| [`addons/web/controllers/home.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/home.py#L1) | `Home`; `Home.web_login` |
| [`addons/web/controllers/report.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/report.py#L1) | `ReportController` |
| [`addons/web/static/src/core/network/rpc.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/network/rpc.js#L1) | `rpcBus`; `RPCError`; `ConnectionLostError`; `ConnectionAbortedError`; `RequestEntityTooLargeError`; `makeErrorFromResponse`; `rpc` |
| [`addons/web/static/src/core/orm_service.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/orm_service.js#L1) | `x2ManyCommands`; `UPDATE_METHODS`; `ORM`; `ormService` |
| [`addons/web/static/src/core/registry.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/registry.js#L1) | `KeyNotFoundError`; `DuplicatedKeyError`; `is`; `this`; `Registry`; `registry` |
| [`addons/web/static/src/core/utils/hooks.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/utils/hooks.js#L1) | `useAutofocus`; `useBus`; `useServiceProtectMethodHandling`; `SERVICES_METADATA`; `useService`; `useSpellCheck`; `useChildRef`; `useForwardRefToParent`; `useOwnedDialogs`; `useRefListener` |
| [`addons/web/static/src/core/utils/patch.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/utils/patch.js#L1) | `A`; `patch`; `A`; `prototype` |
| [`addons/web/static/src/views/fields/char/char_field.js` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/views/fields/char/char_field.js#L1) | `CharField`; `charField` |
| [`addons/website/controllers/main.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/controllers/main.py#L1) | `QueryURL`; `Website`; `Website.web_login`; `WebsiteSession`; `WebsiteBinary` |
| [`addons/website/models/mixins.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/models/mixins.py#L1) | `WebsiteSeoMetadata`; `WebsiteCover_PropertiesMixin`; `WebsiteCover_PropertiesMixin.write`; `WebsitePageVisibilityOptionsMixin`; `WebsitePageOptionsMixin`; `WebsiteMultiMixin`; `WebsitePublishedMixin`; `WebsitePublishedMixin.create`; `WebsitePublishedMixin.write`; `WebsitePublishedMultiMixin`; `WebsiteSearchableMixin` |
| [`addons/website/models/website.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/models/website.py#L1) | `Website`; `Website.create`; `Website.write` |
| [`addons/website/models/website_page.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/models/website_page.py#L1) | `PageCannotBeCached`; `WebsitePage`; `WebsitePage.write` |
| [`addons/website_sale/controllers/main.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/main.py#L1) | `handle_product_params_error`; `TableCompute`; `WebsiteSale`; `WebsiteSale._prepare_product_values`; `WebsiteSale._prepare_breadcrumb_markup_data`; `WebsiteSale._prepare_checkout_page_values`; `WebsiteSale._prepare_address_form_values`; `WebsiteSale._prepare_address_update`; `WebsiteSale._prepare_shop_payment_confirmation_values` |
| [`odoo/addons/base/models/ir_actions.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_actions.py#L1) | `LoggerProxy`; `IrActionsActions`; `IrActionsActions.create`; `IrActionsActions.write`; `IrActionsAct_Window`; `IrActionsAct_Window.create`; `IrActionsAct_WindowView`; `IrActionsAct_Window_Close`; `IrActionsAct_Url`; `ServerActionHistoryWizard`; `IrActionsServerHistory`; `ServerActionWithWarningsError`; `IrActionsServer`; `IrActionsServer.create`; `IrActionsServer.write`; `IrActionsTodo`; `IrActionsTodo.create`; `IrActionsTodo.write`; `IrActionsClient` |
| [`odoo/addons/base/models/ir_actions_report.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_actions_report.py#L1) | `_run_wkhtmltopdf`; `_split_table`; `WkhtmlInfo`; `_wkhtml`; `IrActionsReport`; `IrActionsReport._prepare_html`; `IrActionsReport._prepare_pdf_report_attachment_vals_list`; `IrActionsReport.report_action`; `IrActionsReport._prepare_local_attachments` |
| [`odoo/addons/base/models/ir_asset.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_asset.py#L1) | `fs2web`; `can_aggregate`; `is_wildcard_glob`; `_glob_static_file`; `IrAsset`; `IrAsset.create`; `IrAsset.write`; `AssetPaths` |
| [`odoo/addons/base/models/ir_attachment.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_attachment.py#L1) | `condition_values`; `IrAttachment`; `IrAttachment.write`; `IrAttachment.create` |
| [`odoo/addons/base/models/ir_binary.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_binary.py#L1) | `IrBinary` |
| [`odoo/addons/base/models/ir_config_parameter.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_config_parameter.py#L1) | `IrConfig_Parameter`; `IrConfig_Parameter.create`; `IrConfig_Parameter.write` |
| [`odoo/addons/base/models/ir_cron.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_cron.py#L1) | `BadVersion`; `BadModuleState`; `CompletionStatus`; `ListLogHandler`; `IrCron`; `IrCron.create`; `IrCron.write`; `IrCron._commit_progress`; `IrCronTrigger`; `IrCronProgress` |
| [`odoo/addons/base/models/ir_model.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_model.py#L1) | `make_compute`; `mark_modified`; `model_xmlid`; `field_xmlid`; `selection_xmlid`; `query_insert`; `query_update`; `select_en`; `upsert_en`; `Base`; `Unknown`; `IrModel`; `IrModel.write`; `IrModel.create`; `IrModelFields`; `IrModelFields._prepare_update`; `IrModelFields.create`; `IrModelFields.write`; `IrModelInherit`; `IrModelFieldsSelection`; `IrModelFieldsSelection.create`; `IrModelFieldsSelection.write` |
| [`odoo/addons/base/models/ir_qweb.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_qweb.py#L1) | `_id_or_xmlid`; `indent_code`; `keep_query`; `QWebError`; `QWebErrorInfo`; `QwebCallParameters`; `QwebStackFrame`; `QwebContent`; `QwebJSON`; `IrQweb`; `IrQweb._prepare_environment`; `render` |
| [`odoo/addons/base/models/ir_rule.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_rule.py#L1) | `IrRule`; `IrRule.create`; `IrRule.write` |
| [`odoo/addons/base/models/ir_sequence.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_sequence.py#L1) | `_create_sequence`; `_drop_sequences`; `_alter_sequence`; `_select_nextval`; `_update_nogap`; `_predict_nextval`; `IrSequence`; `IrSequence.create`; `IrSequence.write`; `IrSequenceDate_Range`; `IrSequenceDate_Range.create`; `IrSequenceDate_Range.write` |
| [`odoo/addons/base/models/ir_ui_view.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_ui_view.py#L1) | `att_names`; `IrUiViewCustom`; `_hasclass`; `get_view_arch_from_file`; `IrUiView`; `IrUiView.create`; `IrUiView.write`; `ResetViewArchWizard`; `Base`; `NameManager` |
| [`odoo/addons/base/models/res_config.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/res_config.py#L1) | `ResConfig`; `ResConfigSettings`; `ResConfigSettings.create` |
| [`odoo/addons/base/models/res_users.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/res_users.py#L1) | `CryptContext`; `_jsonable`; `check_identity`; `ResUsersLog`; `ResUsers`; `ResUsers.create`; `ResUsers.write`; `ResUsers.authenticate`; `UsersMultiCompany`; `UsersMultiCompany.create`; `UsersMultiCompany.write`; `ResUsersIdentitycheck`; `ChangePasswordWizard`; `ChangePasswordUser`; `ChangePasswordOwn`; `ResUsersApikeys`; `_check_apikey_credentials`; `ResUsersApikeysDescription`; `ResUsersApikeysDescription.create`; `ResUsersApikeysShow` |
| [`odoo/http.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L1) | `get_default_session`; `RegistryError`; `SessionExpiredException`; `content_disposition`; `db_list`; `db_filter`; `dispatch_rpc`; `get_session_max_inactivity`; `is_cors_preflight`; `serialize_exception`; `fragment_to_query_string`; `Stream`; `Controller`; `route`; `_generate_routing_rules`; `_check_and_complete_route_definition`; `FilesystemSessionStore`; `Session`; `Session.authenticate`; `GeoIP`; `borrow_request`; `make_request_wrap_methods` |
| [`odoo/modules/loading.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/loading.py#L1) | `load_data`; `load_demo`; `force_demo`; `load_module_graph`; `_check_module_names`; `load_modules`; `reset_modules_state` |
| [`odoo/modules/migration.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/migration.py#L1) | `MigrationManager`; `exec_script` |
| [`odoo/orm/commands.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/commands.py#L1) | `Command`; `Command.create` |
| [`odoo/orm/decorators.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/decorators.py#L1) | `attrsetter`; `constrains`; `constrains`; `constrains`; `ondelete`; `onchange`; `depends`; `depends`; `depends`; `depends_context`; `autovacuum`; `model`; `private`; `readonly`; `model_create_multi` |
| [`odoo/orm/domains.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/domains.py#L1) | `OptimizationLevel`; `Domain`; `DomainBool`; `DomainNot`; `DomainNary`; `DomainAnd`; `DomainOr`; `DomainCustom`; `DomainCondition`; `operator_optimization`; `field_type_optimization`; `_optimize_nary_sort_key`; `nary_optimization`; `nary_condition_optimization`; `_operator_equal_if_value`; `_operator_different`; `_operator_equals`; `_operator_equal_as_in`; `_optimize_in_set`; `_optimize_in_required`; `_optimize_any_domain`; `_optimize_any_domain_at_level` |
| [`odoo/orm/fields.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/fields.py#L1) | `resolve_mro`; `determine`; `Field`; `Field.create`; `Field.write` |
| [`odoo/orm/fields_relational.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/fields_relational.py#L1) | `_Relational`; `Many2one`; `Many2one.write`; `_RelationalMulti`; `_RelationalMulti.create`; `_RelationalMulti.write`; `One2many`; `Many2many`; `PrefetchMany2one`; `PrefetchX2many` |
| [`odoo/orm/models.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L1) | `parse_read_group_spec`; `raise_on_invalid_object_name`; `fix_import_export_id_paths`; `to_record_ids`; `check_company_domain_parent_of`; `check_companies_domain_parent_of`; `MetaModel`; `BaseModel`; `BaseModel.check_access`; `BaseModel.write`; `BaseModel.create`; `BaseModel._prepare_create_values`; `RecordCache`; `Model`; `ReversibleComparator`; `itemgetter_tuple`; `get_columns_from_sql_diagnostics` |
| [`odoo/orm/models_transient.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models_transient.py#L1) | `TransientModel` |
| [`odoo/orm/registry.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/registry.py#L1) | `_unaccent`; `Registry`; `DummyRLock`; `TriggerTree` |
| [`odoo/service/model.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/service/model.py#L1) | `Params`; `get_public_method`; `call_kw`; `dispatch`; `execute_cr`; `retrying`; `_traverse_containers` |
| [`odoo/tests/common.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tests/common.py#L1) | `__getattr__`; `get_db_name`; `RegistryRLock`; `release_test_lock`; `standalone`; `test_xsd`; `new_test_user`; `loaded_demo_data`; `RecordCapturer`; `_enter_context`; `_normalize_arch_for_assert`; `BlockedRequest`; `BaseCase`; `Like`; `WhitespaceInsensitive`; `Approx`; `TransactionCase`; `SingleTransactionCase`; `ChromeBrowserException`; `run`; `save_test_file`; `ChromeBrowser` |
| [`odoo/tools/profiler.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tools/profiler.py#L1) | `_format_frame`; `_format_stack`; `get_current_frame`; `_get_stack_trace`; `stack_size`; `make_session`; `force_hook`; `Collector`; `SQLCollector`; `_BasePeriodicCollector`; `PeriodicCollector`; `SyncCollector`; `QwebTracker`; `QwebCollector`; `ExecutionContext`; `Profiler`; `Nested` |
| [`odoo/upgrade_code/17.5-01-tree-to-list.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/17.5-01-tree-to-list.py#L1) | `upgrade` |
| [`odoo/upgrade_code/18.1-00-sql-constraint.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-00-sql-constraint.py#L1) | `upgrade` |
| [`odoo/upgrade_code/18.1-02-route-jsonrpc.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-02-route-jsonrpc.py#L1) | `upgrade` |

## Complément de preuve : agrégations web

`addons/web/models/models.py`, `Base.formatted_read_group`, récupéré au même SHA 19. Ce complément résout la lacune repérée pendant l’essai de portage.
