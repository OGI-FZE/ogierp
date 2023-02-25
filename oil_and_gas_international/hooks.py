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
    "Sales Order": "public/js/sales_order.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Supplier Quotation": "public/js/supplier_quotation.js",
    "Project": "public/js/project.js",
    "Quotation": "public/js/quotation.js",
    "Job Card": "public/js/Job Card.js",
    "Work Order": "public/js/work_order.js"
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

override_doctype_class = {
	"Work Order": "oil_and_gas_international.overriding.CustomWorkOrder"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    # "Asset": {
    #     "on_submit": "oil_and_gas_international.events.asset.on_submit",
    #     "on_cancel": "oil_and_gas_international.events.asset.remove_from_tubular"
    # },
    "Sales Invoice": {
        "on_submit": "oil_and_gas_international.events.sales_invoice.addbilledamount",
        "on_cancel": "oil_and_gas_international.events.sales_invoice.removebilledamount",
        "validate": "oil_and_gas_international.events.sales_invoice.get_desc",
    #     "on_submit": "oil_and_gas_international.events.sales_invoice.on_submit"
    },
	"Sales Order": {
		"on_submit": "oil_and_gas_international.events.sales_order.create_project"
	},
	"Project": {
		"validate": "oil_and_gas_international.tasks.aft_project"
	},
    "Job Card": {
        "on_submit": "oil_and_gas_international.events.job_card.create_job_card_against_wo",
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "cron": {
        "* * * * *": [
            "frappe.email.queue.flush"
        ],

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
                'Item-other_item_type',
                'Item-relevant_item',
                #Custom Section
                'Item-specifications',
                'Item-hs_code',
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
                'Item-stud_bolt_size_lh_',
                'Item-gasket_size_lh_',
                'Item-packer_size',
                'Item-used_for',
                'Item-style',
                'Item-packing_element',
                'Item-ss_ring_groove_',
                'Item-no_of_stud_bolts_rh',
                'Item-stud_bolt_size_rh',
                'Item-gasket_size_rh_',
                'Item-pressure_rating_rh',
                'Item-no_of_stud_bolts_lh_',
                'Item-hard_banding_',
                'Item-service',
                'Item-slip_recess_',
                'Item-elvator_recess',
                'Item-bottom_connection',
                'Item-top_connection',
                'Item-plastic_coating',
                'Item-od_size_',
                'Item-tool_joint_id',
                'Item-parent_group',
                'Item-grand_parent_group',
                'Item-is_exempt',
                'Item-is_zero_rated',
                'Item-tax_code',
                'Item-is_string',
                'Item-assets_available_for_rent',
                'Item-assets_in_use',
                'Item-total_assets',
                'Item-string_details',
                'Item-usage_status',

                # Opportunity
                'Opportunity-references',
                'Opportunity-rental_estimation',
                'Opportunity-sales_person',
                'Opportunity-departments',

                # Opportunity Item

                # Material Request Item
                'Material Request Item-rental_order',

                # Materi Request
                'Material Request-rental_order',

                # Purchase Order
                'Purchase Order-rental_order',
                'Purchase Order-supplier_rental_timesheet',
                'Purchase Order-supplier_rental_order',

                # Purchase Order Item
                'Purchase Order Item-rental_order',
                'Purchase Order Item-assets',
                'Purchase Order Item-asset_item',
                'Purchase Order Item-supplier_rental_order_item',
                'Purchase Order Item-supplier_rental_order',

                # Purcahse Invoice
                'Purchase Invoice-rental_order',
                'Purchase Invoice-supplier_rental_timesheet',
                'Purchase Invoice-supplier_rental_order',

                # purchase Invoice Item
                'Purchase Invoice Item-rental_order',
                'Purchase Invoice Item-rental_order_item',
                'Purchase Invoice Item-assets',
                'Purchase Invoice Item-asset_item',
                'Purchase Invoice Item-supplier_rental_order_item',
                'Purchase Invoice Item-supplier_rental_order',

                # Sales Invoice
                "Sales Invoice-rental_references",
                "Sales Invoice-rental_order",
                "Sales Invoice-rental_order_item",
                "Sales Invoice-rental_timesheet",
                "Sales Invoice-rental_timesheet_item",
                "Sales Invoice-rental_order",
                "Sales Invoice-departments",
                #Sales Invoie Item
                'Sales Invoice Item-asset_item',
                'Sales Invoice Item-rental_order_item',
                'Sales Invoice Item-rental_order',
                'Sales Invoice Item-details',
                'Sales Invoice Item-assets',
                'Sales Invoice Item-asset_qty',
                'Sales Invoice Item-unit_price',
                'Sales Invoice Item-child_category',
                'Sales Invoice Item-days',
                'Sales Invoice-aed_exchange_rate',

                # Stock Entry
                "Stock Entry-against_asset_formation",

                #Sales Order
                'Sales Order Item-assets','Sales Order-rental_timesheet_item','Sales Order-rental_order_item',
                'Sales Order-rental_timesheet','Sales Order-rental_order','Sales Order Item-rental_order',
                'Sales Order Item-rental_order_item','Sales Order Item-references','Sales Order Item-asset_item',
                'Sales Order-aed_exchange_rate',

                # Project
                'Project-rental_order','Project-sub_rental_order',

                #Rental order
                'Rental Order-sales_employee','Rental Order-sales_person_link',
                'Rental Order-sales_person_name','Rental Order-remarks','Rental Order-freight',
                'Rental Order-client_terms','Rental Order-credit_limit','Rental Order-payment_terms','Rental Order-delivery_terms',
                'Rental Order-prices','Rental Order-delivery_date','Rental Order-mail_id','Rental Order-contact_number','Rental Order-sales_person_details',
                'Rental Order-client_po_date','Rental Order-client_po_no',

                #Rental quotation
                'Rental Quotation-sales_person','Rental Quotation-departments',

                #Asset Movement
                'Asset Movement-rental_issue_note','Asset Movement-sub_rental_issue_note',

                #dn
                'Delivery Note-commercial_invoice_date',
                
                #employee
                'Employee-visa_expiry_date','Employee-visa_issue_date','Employee-visa_no',
                #bom
                'BOM Operation-reference_std',
                #workorder
                'Work Order Operation-reference_std','Work Order Operation-acceptance_criteria',
                'Work Order-raw_material_details','Work Order-bar_heat_no','Work Order-acceptance_standard',
                'Work Order-material_grade_spec','Work Order-uom','Work Order-date',
                #Quotation
                'Quotation-aed_exchange_rate','Quotation-email','Quotation-contact','Quotation-sales_person',
                #sales person
                'Sales Person-email','Sales Person-contact',

                #purchase receipt
                'Purchase Receipt-reason_for_purchase',
                'Quotation-estimation_sheet'

            ]]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["name", "in", [
                # Item
                'Item-item_group-label','Project-main-quick_entry','Project-naming_series-options'
            ]]
        ]
    },

]
