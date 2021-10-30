
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "against_asset_formation",
        "transactions": [
            {
                'label': _('References'),
                'items': ['Asset', "Stock Entry"]
            },
        ]
    }
