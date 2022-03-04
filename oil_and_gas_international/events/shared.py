import frappe


@frappe.whitelist()
def get_lost_and_damage_prices(item_code=None):
    if not item_code:
        return 0, 0

    lihdbr = 0
    oprunning = 0
    standby = 0
    redress = 0
    straight = 0
    post_rental_inspection_charges = 0

    rd_settings = frappe.get_single("Rental Division Settings")

    if rd_settings.lih_dbr:
        lihdbr = frappe.get_value("Item Price", {
            "price_list": rd_settings.lih_dbr,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.operational_running:
        oprunning = frappe.get_value("Item Price", {
            "price_list": rd_settings.operational_running,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.standby:
        standby = frappe.get_value("Item Price", {
            "price_list": rd_settings.standby,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.redress:
        redress = frappe.get_value("Item Price", {
            "price_list": rd_settings.redress,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.straight:
        straight = frappe.get_value("Item Price", {
            "price_list": rd_settings.straight,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.post_rental_inspection_charges:
        post_rental_inspection_charges = frappe.get_value("Item Price", {
            "price_list": rd_settings.post_rental_inspection_charges,
            "item_code": item_code
        }, "price_list_rate")

    return oprunning, standby , lihdbr, redress, straight, post_rental_inspection_charges
