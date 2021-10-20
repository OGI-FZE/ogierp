import frappe
from oil_and_gas_international.events.rental_estimation import check_validity as check_re_validity
from oil_and_gas_international.events.rental_quotation import check_validity as check_rq_validity


def daily():
    check_re_validity()
    check_rq_validity()
