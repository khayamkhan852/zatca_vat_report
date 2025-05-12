// Copyright (c) 2025, Khayam Khan and contributors
// For license information, please see license.txt

frappe.query_reports["Journal VAT Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_default("company"),
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
		{
			'fieldname': 'voucher_number',
			'label': __('Voucher Number'),
			'fieldtype': 'Link',
			'options': 'Journal Entry',
			'get_query': function() {
				return {
					filters: {
						docstatus: 1,
						custom_is_vat_entry: 1,
						company: frappe.query_report.get_filter_value('company')
					}
				};
			}
		},
	]
};
