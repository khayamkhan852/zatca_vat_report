# Copyright (c) 2025, Khayam Khan and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()

	data = get_data(filters)
	
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "posting_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "supplier",
			"label": _("Particular"),
			"fieldtype": "Data",
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
			"width": 120
		},
		{
			"fieldname": "voucher_number",
			"label": _("Voucher Number"),
			"fieldtype": "Link",
			"options": "Journal Entry",
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

def get_data(filters):
	conditions = get_conditions(filters)

	journal_entries = frappe.get_all(
		"Journal Entry",
		fields=[
			"name", 
			"posting_date", 
			"custom_supplier_namecashbank_purchase", 
			"custom_vat_no", 
		],
		filters=conditions
	)

	data = []
	for journal_entry in journal_entries:
		tax_amount = 0
		taxable_amount = 0

		accounts = frappe.get_all("Journal Entry Account",
			fields=[
				"custom_entry_type", 
				"debit_in_account_currency", 
			],
			filters=[
				["parent", "=", journal_entry.name],
				["custom_entry_type", "in", ["Taxable Amount", "Tax Amount"]],
			]
		)


		for journal_entry_account in accounts:
			if journal_entry_account.custom_entry_type == "Taxable Amount":
				taxable_amount = journal_entry_account.debit_in_account_currency
			elif journal_entry_account.custom_entry_type == "Tax Amount":
				tax_amount = journal_entry_account.debit_in_account_currency

		data.append({
            "posting_date": journal_entry.posting_date,
            "supplier": journal_entry.custom_supplier_namecashbank_purchase,
            "tax_id": journal_entry.custom_vat_no,
			'voucher_type': "Journal Entry",
			"voucher_number": journal_entry.name,
			"taxable_amount": taxable_amount,
			"tax_amount": tax_amount
        })	

	return data

def get_conditions(filters):
	journal_entry_filters = {
		"docstatus": 1,
		"custom_is_vat_entry" : 1,
		"company": filters.get("company"),
	}

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		journal_entry_filters["posting_date"] = ["between", [from_date, to_date]]

	if filters.get("voucher_number"):
		journal_entry_filters["name"] = filters.get("voucher_number")

	return journal_entry_filters


