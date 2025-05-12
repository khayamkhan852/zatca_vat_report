# Copyright (c) 2025, Khayam Khan and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	
	data = get_data(filters)

	return columns, data


def get_columns():
	columns = [
		{
			"fieldname": "posting_date",
			"label":  _("Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "customer",
			"label":  _("Particular"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "custom_vat_registration_number",
			"label":  _("VAT Number"),
			"fieldtype": "data",
			"width": 170
		},
		{
			"fieldname": "voucher_type",
			"label":  _("Voucher Type"),
			"fieldtype": "data",
			"width": 100
		},
		{
			"fieldname": "voucher_number",
			"label":  _("Voucher Number"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200
		},
		{
			"fieldname": "taxable_amount",
			"label":  _("Taxable Amount"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "tax_amount",
			"label":  _("Tax Amount"),
			"fieldtype": "Currency",
			"width": 200
		}
	]

	return columns

def get_data(filters=None):
	invoice_filters = {
		"docstatus": 1,
		"company": filters.get("company"),
	}

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		invoice_filters["posting_date"] = ["between", [from_date, to_date]]

	if filters.get("voucher_type"):
		if filters.get("voucher_type") == "E-Invoice":
			invoice_filters["is_return"] = 0
		elif filters.get("voucher_type") == "Credit Note":
			invoice_filters["is_return"] = 1

	if filters.get("voucher_number"):
		invoice_filters["name"] = filters.get("voucher_number")		

	if filters.get('particular'):
		invoice_filters["customer"] = filters.get('particular')

	sales_invoices = frappe.get_all(
		"Sales Invoice",
		fields=["name", "posting_date", "customer", "is_return", "total", "total_taxes_and_charges"],
		filters=invoice_filters
	)

	data = []
	for invoice in sales_invoices:
		vat_number = frappe.db.get_value("Customer", invoice.customer, "custom_vat_registration_number")
		data.append({
            "posting_date": invoice.posting_date,
            "customer": invoice.customer,
            "custom_vat_registration_number": vat_number,
			'voucher_type': "E-Invoice" if not invoice.is_return else "Credit Note",
			"voucher_number": invoice.name,
			"taxable_amount": invoice.total,
			"tax_amount": invoice.total_taxes_and_charges
        })

	return data