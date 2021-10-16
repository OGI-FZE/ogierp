import frappe
from oil_and_gas_international.events.rental_estimation import check_validity as check_re_validity


def daily():
    check_re_validity()
