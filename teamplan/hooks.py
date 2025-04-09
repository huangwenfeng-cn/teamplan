app_name = "teamplan"
app_title = "teamplan"
app_publisher = "Frappe Technologies Pvt Ltd"
app_description = "Team discussion and collaboration tool"
app_email = "faris@frappe.io"
app_license = "AGPLv3"
app_icon_url = "/assets/teamplan/manifest/favicon-180.png"
app_icon_title = "teamplan"
app_icon_route = "/g"

add_to_apps_screen = [
	{
		"name": "teamplan",
		"logo": "/assets/teamplan/manifest/favicon-196.png",
		"title": "teamplan",
		"route": "/g",
		# "has_permission": "teamplan.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/teamplan/css/teamplan.css"
# app_include_js = "/assets/teamplan/js/teamplan.js"

# include js, css files in header of web template
# web_include_css = "/assets/teamplan/css/teamplan.css"
# web_include_js = "/assets/teamplan/js/teamplan.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "teamplan/public/scss/website"

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

# Fixtures

fixtures = [
	{"dt": "Role", "filters": [["role_name", "like", "teamplan %"]]},
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

website_route_rules = [
	{"from_route": "/g/<path:app_path>", "to_route": "g"},
]

website_redirects = [
	{"source": r"/teams(/.*)?", "target": r"/g\1"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "teamplan.utils.jinja_methods",
# 	"filters": "teamplan.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "teamplan.install.before_install"
after_install = "teamplan.install.after_install"

after_migrate = ["teamplan.search.build_index_in_background"]

# Uninstallation
# ------------

# before_uninstall = "teamplan.uninstall.before_uninstall"
# after_uninstall = "teamplan.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "teamplan.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
has_permission = {"GP Page": "teamplan.teamplan.doctype.gp_page.gp_page.has_permission"}

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
	"*": {
		"on_trash": "teamplan.mixins.on_delete.on_trash",
	},
	"User": {
		"after_insert": "teamplan.teamplan.doctype.gp_user_profile.gp_user_profile.create_user_profile",
		"on_trash": [
			"teamplan.teamplan.doctype.gp_user_profile.gp_user_profile.delete_user_profile",
			"teamplan.teamplan.doctype.gp_guest_access.gp_guest_access.on_user_delete",
		],
		"on_update": "teamplan.teamplan.doctype.gp_user_profile.gp_user_profile.on_user_update",
	},
}

on_login = "teamplan.www.g.on_login"

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": ["teamplan.search.build_index_if_not_exists"],
	"hourly": ["teamplan.teamplan.doctype.gp_invitation.gp_invitation.expire_invitations"],
}

# scheduler_events = {
# 	"all": [
# 		"teamplan.tasks.all"
# 	],
# 	"daily": [
# 		"teamplan.tasks.daily"
# 	],
# 	"hourly": [
# 		"teamplan.tasks.hourly"
# 	],
# 	"weekly": [
# 		"teamplan.tasks.weekly"
# 	],
# 	"monthly": [
# 		"teamplan.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "teamplan.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.client.get_list": "teamplan.extends.client.get_list"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "teamplan.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


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
# 	"teamplan.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
