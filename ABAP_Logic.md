###DATABASE TABLES:

1. Sales Header Table:

```abap
   define table zsales_header_sp {

  key client      : abap.clnt not null;
  key order_uuid  : sysuuid_x16 not null;
  @EndUserText.label : 'Sales Order ID'
  sales_id        : abap.char(10);
  @EndUserText.label : 'Customer ID'
  customer_id     : abap.char(10);
  @EndUserText.label : 'Order Status'
  overall_status  : abap.char(1);
  created_at      : abp_creation_tstmpl;
  last_changed_at : abp_lastchange_tstmpl;

}
```
 2. Sales Item Table:
```abap

   define table zsales_item_sp {

  key client    : abap.clnt not null;
  key item_uuid : sysuuid_x16 not null;
  parent_uuid   : sysuuid_x16 not null;
  @EndUserText.label : 'Product ID'
  product_id    : abap.char(20);
  @EndUserText.label : 'Price'
  @Semantics.amount.currencyCode : 'zsales_item_sp.currency_code'
  price         : abap.curr(15,2);
  @EndUserText.label : 'Currency'
  currency_code : abap.cuky;
  @EndUserText.label : 'Quantity'
  quantity      : abap.int4;
  @EndUserText.label : 'Planned Delivery'
  planned_date  : abap.dats;
  @EndUserText.label : 'Actual Delivery'
  actual_date   : abap.dats;

}
```

###CORE DATA SERVICES

1. Sales Header Root View

```abap

define root view entity ZI_SALES_HEADER_SP
  as select from zsales_header_sp -- Points to your Table
  composition [0..*] of zi_sales_item_sp as _Items
{
  key order_uuid      as OrderUuid,
      sales_id        as SalesId,
      customer_id     as CustomerId,
      overall_status  as OverallStatus,
      created_at      as CreatedAt,
      last_changed_at as LastChangedAt,
      
      _Items -- Exposes the items for nested analysis
}
```

2. Sales Item Root View

```abap
define view entity ZC_SALES_ITEM_SP
  as projection on ZI_SALES_ITEM_SP
{
    key ItemUuid,
    ParentUuid,
    
    @UI.lineItem: [{ position: 10 }]
    ProductId,
    
    @UI.lineItem: [{ position: 20 }]
    @Semantics.amount.currencyCode: 'CurrencyCode'
    Price,
    
    CurrencyCode,
    
    @UI.lineItem: [{ position: 30 }]
    Quantity,
    
    @UI.lineItem: [{ position: 40 }]
    DelayDays,

    /* Link back to parent */
    _SalesHeader : redirected to parent ZC_SALES_HEADER_SP
}


```

3. Sales Header Consumotion View
```abap
define root view entity ZI_SALES_HEADER_SP
  as select from zsales_header_sp -- Points to your Table
  composition [0..*] of zi_sales_item_sp as _Items
{
  key order_uuid      as OrderUuid,
      sales_id        as SalesId,
      customer_id     as CustomerId,
      overall_status  as OverallStatus,
      created_at      as CreatedAt,
      last_changed_at as LastChangedAt,
      
      _Items -- Exposes the items for nested analysis
}

```
4. Sales Item Consumption View
```abap
define view entity ZI_SALES_ITEM_SP
  as select from ZSALES_ITEM_SP -- Points to your Table
  association to parent ZI_SALES_HEADER_SP as _SalesHeader on $projection.ParentUuid = _SalesHeader.OrderUuid
{
  key item_uuid     as ItemUuid,
      parent_uuid   as ParentUuid,
      product_id    as ProductId,
      @Semantics.amount.currencyCode: 'CurrencyCode'
      price         as Price,
      currency_code as CurrencyCode,
      quantity      as Quantity,
      planned_date  as PlannedDate,
      actual_date   as ActualDate,
      
      /* Calculation for the Analytics Dashboard */
      case 
        when actual_date = '00000000' then 0
        else dats_days_between(planned_date, actual_date) 
      end           as DelayDays,

      _SalesHeader -- Exposes the association
}
```
###SERVICE DEFINITION

```abap
define service ZUI_SALES_ANALYTICS_SP {
  expose ZC_SALES_HEADER_SP as SalesHeader;
  expose ZC_SALES_ITEM_SP   as SalesItems;
}
```

###SERVICE BINDING
```
Binding Type: OData V4 - UI
Service Name: Z_UI_SALES_SP_V4
```
