import frappe

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
            'remarks': f'Asset Convertion against Asset#{doc.name}'
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
                serial_no.customer = row.customer
                serial_no.save()
            else:
                if not row.for_asset:
                    all_assets_created = False

        # Validating if all Assets have been created
        if all_assets_created:
            asset_formation.db_set('status', 'Assets Created')

        frappe.msgprint(f'Stock Entry# {stock_entry.name} Created')
        frappe.msgprint(f'Serial No {doc.asset_name} status updated')

