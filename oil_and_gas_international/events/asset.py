import frappe
from frappe.utils import today 
from frappe.utils import now_datetime

def on_submit(doc,method):
    create_stock_entry_for_asset_conversion(doc,method)
    update_string_item(doc,method)

def update_string_item(doc,method):
    item_doc = frappe.get_doc("Item",doc.item_code)
    if item_doc and item_doc.is_string:
        total_assets = item_doc.total_assets + 1
        frappe.db.set_value("Item",doc.item_code,'total_assets',total_assets)
        frappe.db.set_value("Item",doc.item_code,'assets_available_for_rent',(total_assets - item_doc.assets_in_use))

def remove_from_tubular(doc,method):
    item_doc = frappe.get_doc("Item",doc.item_code)
    if item_doc and item_doc.is_string:
        total_assets = item_doc.total_assets - 1
        frappe.db.set_value("Item",doc.item_code,'total_assets',total_assets)
        frappe.db.set_value("Item",doc.item_code,'assets_available_for_rent',(total_assets - item_doc.assets_in_use))

def create_stock_entry_for_asset_conversion (doc, method):
    '''
    Creates a Stock Entry to remove the value from Stock in Hand to Asset Account if linked with Asset Formation
    '''    
    if doc.against_asset_formation:
        # getting asset account
        fixed_asset_account = frappe.get_value('Asset Category Account', {
                'company_name' : doc.company, 
                'parent': doc.asset_category
                }, ['fixed_asset_account'])
        
        # Creating new Stock Entry
        stock_entry = frappe.get_doc({
            'doctype': 'Stock Entry',
            'stock_entry_type': 'Material Issue',
            'posting_date': doc.purchase_date,
            'asset': doc.name,
            'company': doc.company,
            'remarks': f'Asset Convertion against Asset#{doc.name}',
            'against_asset_formation': doc.against_asset_formation
            })

        # Entry for Stock Item
        asset_formation = frappe.get_doc('Asset Formation', doc.against_asset_formation)
        stock_entry.append('items', {
            's_warehouse': asset_formation.warehouse,
            'item_code': asset_formation.item_code,
            'qty': 1,
            'serial_no': doc.asset_name,
            'expense_account': fixed_asset_account
        })

        stock_entry.insert()
        stock_entry.submit()

        # Updating Asset Formation Doc
        all_assets_created = True
        for row in asset_formation.items:
            if row.serial_no == doc.asset_name:
                item_doc = frappe.get_doc('Asset Formation Item', row.name)
                item_doc.db_set('for_asset', doc.name)

                # Updating Serial Number Status
                serial_no = frappe.get_doc('Serial No', doc.asset_name)
                serial_no.status = 'Converted To Asset'
                serial_no.save()
            else:
                if not row.for_asset:
                    all_assets_created = False

        # Validating if all Assets have been created
        if all_assets_created:
            asset_formation.db_set('status', 'Assets Created')

        frappe.msgprint(f'Stock Entry# {stock_entry.name} Created')
        frappe.msgprint(f'Serial No {doc.asset_name} status updated')

@frappe.whitelist()
def set_initial_location(asset=None):
    asset_doc = frappe.get_doc("Asset",asset)
    current_loc = asset_doc.location
    init_loc = frappe.db.sql("""select tami.target_location from `tabAsset Movement` tam join `tabAsset Movement Item` tami on tam.name=tami.parent where
        tami.asset='{0}' and tam.purpose='Receipt' and tam.docstatus=1""".format(asset))
    init_loc = init_loc[0][0]

    if init_loc:
        # asset movement to put it back in initial location
        if current_loc != init_loc:
            asset_movement_doc = frappe.get_doc({
                "doctype": "Asset Movement",
                "transaction_date": now_datetime(),
                "purpose": "Transfer"
            })
            asset_movement_doc.append("assets", {
                "asset": asset,
                "source_location": current_loc,
                "target_location": init_loc
            })
            asset_movement_doc.save()
            asset_movement_doc.submit()

        frappe.db.commit()
    return init_loc
