import frappe

__version__ = "0.0.1"


def is_guest():
	if frappe.session.user == "Administrator":
		return False
	roles = frappe.get_roles()
	if "teamplan Member" in roles or "teamplan Admin" in roles:
		return False
	return "teamplan Guest" in roles


def refetch_resource(cache_key: str | list, user=None):
	frappe.publish_realtime(
		"refetch_resource", {"cache_key": cache_key}, user=user or frappe.session.user, after_commit=True
	)
