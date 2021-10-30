import frappe


@frappe.whitelist()
def get_lost_and_damage_prices(item_code=None):
    if not item_code:
        return 0, 0

    lost_in_hole_price = 0
    damage_beyond_repair_price = 0

    rd_settings = frappe.get_single("Rental Division Settings")

    if rd_settings.lost_in_hole_price:
        lost_in_hole_price = frappe.get_value("Item Price", {
            "price_list": rd_settings.lost_in_hole_price,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.damage_beyond_repair_price:
        damage_beyond_repair_price = frappe.get_value("Item Price", {
            "price_list": rd_settings.damage_beyond_repair_price,
            "item_code": item_code
        }, "price_list_rate")

    return lost_in_hole_price, damage_beyond_repair_price
