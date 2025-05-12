app_name = "zatca_vat_report"
app_title = "Zatca Vat Report"
app_publisher = "Khayam Khan"
app_description = "Frappe Application that contain VAT Reports For ZATCA"
app_email = "khayamkhan852@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "zatca_vat_report",
# 		"logo": "/assets/zatca_vat_report/logo.png",
# 		"title": "Zatca Vat Report",
# 		"route": "/zatca_vat_report",
# 		"has_permission": "zatca_vat_report.api.permission.has_app_permission"
# 	}
# ]

fixtures = [
    {
        "dt": "Custom Field", "filters": [
            [
                "name", "in", [
                    "Journal Entry Account-custom_entry_type",
                    "Journal Entry-custom_supplier_namecashbank_purchase",
                    'Journal Entry-custom_vat_no',
                    'Journal Entry-custom_section_break_zce99',
                    'Journal Entry-custom_column_break_fy95c',
                    'Journal Entry-custom_supplier_invoice_date',
                    'Journal Entry-custom_column_break_ijdaj',
                    'Journal Entry-custom_is_vat_entry',
                ]
            ]
        ]
    },
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zatca_vat_report/css/zatca_vat_report.css"
# app_include_js = "/assets/zatca_vat_report/js/zatca_vat_report.js"

# include js, css files in header of web template
# web_include_css = "/assets/zatca_vat_report/css/zatca_vat_report.css"
# web_include_js = "/assets/zatca_vat_report/js/zatca_vat_report.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "zatca_vat_report/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "zatca_vat_report/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "zatca_vat_report.utils.jinja_methods",
# 	"filters": "zatca_vat_report.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "zatca_vat_report.install.before_install"
# after_install = "zatca_vat_report.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "zatca_vat_report.uninstall.before_uninstall"
# after_uninstall = "zatca_vat_report.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "zatca_vat_report.utils.before_app_install"
# after_app_install = "zatca_vat_report.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "zatca_vat_report.utils.before_app_uninstall"
# after_app_uninstall = "zatca_vat_report.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zatca_vat_report.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"zatca_vat_report.tasks.all"
# 	],
# 	"daily": [
# 		"zatca_vat_report.tasks.daily"
# 	],
# 	"hourly": [
# 		"zatca_vat_report.tasks.hourly"
# 	],
# 	"weekly": [
# 		"zatca_vat_report.tasks.weekly"
# 	],
# 	"monthly": [
# 		"zatca_vat_report.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "zatca_vat_report.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "zatca_vat_report.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "zatca_vat_report.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["zatca_vat_report.utils.before_request"]
# after_request = ["zatca_vat_report.utils.after_request"]

# Job Events
# ----------
# before_job = ["zatca_vat_report.utils.before_job"]
# after_job = ["zatca_vat_report.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"zatca_vat_report.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

