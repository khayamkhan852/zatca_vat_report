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
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "supplier",
			"label": _("Particular"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 200
		},
		{
			"fieldname": "tax_id",
			"label": _("VAT Number"),
			"fieldtype": "data",
			"width": 170
		},
		{
			"fieldname": "voucher_type",
			"label": _("Voucher Type"),
			"fieldtype": "data",
			"width": 100
		},
		{
			"fieldname": "voucher_number",
			"label": _("Voucher Number"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200
		},
		{
			"fieldname": "taxable_amount",
			"label": _("Taxable Amount"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "tax_amount",
			"label": _("Tax Amount"),
			"fieldtype": "Currency",
			"width": 200
		}
	]

	return columns

def get_data(filters):
	purchase_filters = {
		"docstatus": 1,
		"company": filters.get("company"),
	}

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		purchase_filters["posting_date"] = ["between", [from_date, to_date]]

	if filters.get("particular"):
		purchase_filters["supplier"] = filters.get("particular")

	if filters.get("voucher_number"):
		purchase_filters["name"] = filters.get("voucher_number")

	if filters.get("voucher_type"):
		if filters.get("voucher_type") == "Purchase":
			purchase_filters["is_return"] = 0
		elif filters.get("voucher_type") == "Debit Note":
			purchase_filters["is_return"] = 1

	purchase_invoices = frappe.get_all(
		"Purchase Invoice",
		fields=["name", "posting_date", "supplier", "is_return", "total", "total_taxes_and_charges"],
		filters=purchase_filters
	)

	data = []
	for invoice in purchase_invoices:
		tax_id = frappe.get_value("Supplier", invoice.supplier, "tax_id")

		data.append({
            "posting_date": invoice.posting_date,
            "supplier": invoice.supplier,
            "tax_id": tax_id,
			'voucher_type': "Purchase" if not invoice.is_return else "Debit Note",
			"voucher_number": invoice.name,
			"taxable_amount": invoice.total,
			"tax_amount": invoice.total_taxes_and_charges
        })

	return data			