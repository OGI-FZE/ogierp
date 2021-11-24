from . import __version__ as app_version

app_name = "oil_and_gas_international"
app_title = "Oil And Gas International"
app_publisher = "Havenir Solutions"
app_description = "Oil and Gas International"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/oil_and_gas_international/css/oil_and_gas_international.css"
# app_include_js = "/assets/oil_and_gas_international/js/oil_and_gas_international.js"

# include js, css files in header of web template
# web_include_css = "/assets/oil_and_gas_international/css/oil_and_gas_international.css"
# web_include_js = "/assets/oil_and_gas_international/js/oil_and_gas_international.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "oil_and_gas_international/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Opportunity": "public/js/opportunity.js",
    "Material Request": "public/js/material_request.js",
    "Purchase Order": "public/js/purchase_order.js",
    "Asset": "public/js/asset.js",
    "Item": "public/js/item.js",
    "Sales Invoice": "public/js/sales_invoice.js",
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "oil_and_gas_international.install.before_install"
# after_install = "oil_and_gas_international.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "oil_and_gas_international.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Asset": {
        "on_submit": "oil_and_gas_international.events.asset.create_stock_entry_for_asset_conversion"
    },
    # "Sales Invoice": {
    #     "validate": "oil_and_gas_international.events.sales_invoice.validate",
    #     "on_submit": "oil_and_gas_international.events.sales_invoice.on_submit"
    # },
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "cron": {
        "daily": [
            "oil_and_gas_international.tasks.daily"
        ],
    }
}

# Testing
# -------

# before_tests = "oil_and_gas_international.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "oil_and_gas_international.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "oil_and_gas_international.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"oil_and_gas_international.auth.validate"
# ]

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                # Item
                'Item-item_type',
                'Item-other_item_type',
                'Item-relevant_item',

                # Custom Section
                'Item-specifications',
                'Item-make',
                'Item-model',
                'Item-size',
                'Item-type',
                'Item-part_number',
                'Item-material',
                'Item-pressure_rating',
                'Item-ppf',
                'Item-specifications_col_break_1',
                'Item-pin_box',
                'Item-pin_connection',
                'Item-pin_connection',
                'Item-box_connection',
                'Item-range',
                'Item-oal',
                'Item-od',
                'Item-id',
                'Item-mandrel_od',
                'Item-specifications_col_break_2',
                'Item-stroke',
                'Item-wrap_angle',
                'Item-hard_facing',
                'Item-capacity',
                'Item-degree',
                'Item-psi',
                'Item-torque_guage',
                'Item-lift_cylinders',
                'Item-tool_joint_od',




                # Assets
                'Asset-rental_status',
                'Asset-rental_order',
                'Asset-against_asset_formation',

                # Opportunity
                'Opportunity-item_type',
                'Opportunity-references',
                'Opportunity-rental_estimation',

                # Opportunity Item
                'Opportunity Item-item_type',

                # Material Request Item
                'Material Request Item-rental_order',

                # Materi Request
                'Material Request-rental_order',

                # Purchase Order
                'Purchase Order-rental_order',

                # Purchase Order Item
                'Purchase Order Item-rental_order',

                # Purcahse Invoice
                'Purchase Invoice-rental_order',

                # purchase Invoice Item
                'Purchase Invoice Item-rental_order',
                'Purchase Invoice Item-rental_order_item',

                # Sales Invoice
                "Sales Invoice-rental_references",
                "Sales Invoice-rental_order",
                "Sales Invoice-rental_order_item",
                "Sales Invoice-rental_timesheet",
                "Sales Invoice-rental_timesheet_item",
                "Sales Invoice-rental_order",
                #Sales Invoie Item
                'Sales Invoice Item-asset_item',

                # Stock Entry
                "Stock Entry-against_asset_formation"
            ]]
        ]
    },

]
