// Copyright (c) 2025, Khayam Khan and contributors
// For license information, please see license.txt

frappe.query_reports["VAT Summary Report"] = {
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
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 0
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 0
		},		
	],
	formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (data && data[Object.keys(data)[0]] === "Net Sales" || data[Object.keys(data)[0]] === "Net VAT Payable") {
            value = `<span style="color: green; font-weight: bold;font-size: 15px;">${value}</span>`;
        }

		if (data && data[Object.keys(data)[0]] === "Total Purchase") {
            value = `<span style="color:rgb(137, 5, 203); font-weight: bold;font-size: 15px;">${value}</span>`;
        }

        return value;
    }
};
