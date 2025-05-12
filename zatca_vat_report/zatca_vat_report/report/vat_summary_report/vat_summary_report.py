# # Copyright (c) 2025, Khayam Khan and contributors
# # For license information, please see license.txt

import frappe
from frappe import _
import calendar
import datetime


def execute(filters=None):
    month_labels, year, months = get_months()

    columns = get_columns(month_labels)

    data = get_data(filters, month_labels, months, year)

    return columns, data


def get_columns(month_labels):
    columns = [{
        "fieldname": "particulars",
        "label": _("Particulars"),
        "fieldtype": "Data",
        "width": 250
    }]

    columns += [{
        "fieldname": label,
        "label": _(label),
        "fieldtype": "Currency",
        "width": 190
    } for label in month_labels]

    columns.append({
        "fieldname": "total",
        "label": _("Total"),
        "fieldtype": "Currency",
        "width": 190
    })

    return columns


def get_data(filters, month_labels, months, year):
    rows = {
        "Sales": {},
        "Credit Note (Sales)": {},
        "Net Sales": {},
        "Purchase": {},
        "Purchase (Journal)": {},
        "Total Purchase": {},
        "Purchase Debit": {},
        "Net Purchase": {},
        "Net VAT Payable": {}
    }

    # Totals
    totals = {key: 0 for key in rows}

    for i, month in enumerate(months):
        label = month_labels[i]
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])

        sales = get_sales(filters, start_date, end_date)
        credit = get_credit(filters, start_date, end_date)
        net_sales = round(sales + credit, 2)

        purchase = get_purchase(filters, start_date, end_date)
        journal = get_journal_entries(filters, start_date, end_date)
        total_purchase = round(purchase + journal, 2)

        debit = get_debit(filters, start_date, end_date)
        net_purchase = round(total_purchase + debit, 2)
        net_vat_payable = round(net_sales - net_purchase, 2)

        # Assign values
        rows["Sales"][label] = sales
        rows["Credit Note (Sales)"][label] = -credit
        rows["Net Sales"][label] = net_sales

        rows["Purchase"][label] = purchase
        rows["Purchase (Journal)"][label] = journal
        rows["Total Purchase"][label] = total_purchase
        rows["Purchase Debit"][label] = -debit
        rows["Net Purchase"][label] = net_purchase
        rows["Net VAT Payable"][label] = net_vat_payable

        # Update totals
        totals["Sales"] += sales
        totals["Credit Note (Sales)"] += -credit
        totals["Net Sales"] += net_sales
        totals["Purchase"] += purchase
        totals["Purchase (Journal)"] += journal
        totals["Total Purchase"] += total_purchase
        totals["Purchase Debit"] += -debit
        totals["Net Purchase"] += net_purchase
        totals["Net VAT Payable"] += net_vat_payable

    # Finalize data rows
    data = []
    for key in rows:
        row = {"particulars": key, **rows[key]}
        row["total"] = round(totals[key], 2)
        data.append(row)

    return data


# --- Utility Functions ---

def get_sales(filters, start_date, end_date):
    invoices = frappe.get_all("Sales Invoice", {
        "docstatus": 1,
        "is_return": 0,
        "company": filters.get("company"),
        "posting_date": ["between", [start_date, end_date]]
    }, ["total_taxes_and_charges"])

    return round(sum(inv.total_taxes_and_charges or 0 for inv in invoices), 2)


def get_credit(filters, start_date, end_date):
    credit_notes = frappe.get_all("Sales Invoice", {
        "docstatus": 1,
        "is_return": 1,
        "company": filters.get("company"),
        "posting_date": ["between", [start_date, end_date]]
    }, ["total_taxes_and_charges"])

    return round(sum(inv.total_taxes_and_charges or 0 for inv in credit_notes), 2)


def get_purchase(filters, start_date, end_date):
    purchases = frappe.get_all("Purchase Invoice", {
        "docstatus": 1,
        "is_return": 0,
        "company": filters.get("company"),
        "posting_date": ["between", [start_date, end_date]]
    }, ["total_taxes_and_charges"])

    return round(sum(inv.total_taxes_and_charges or 0 for inv in purchases), 2)


def get_debit(filters, start_date, end_date):
    debits = frappe.get_all("Purchase Invoice", {
        "docstatus": 1,
        "is_return": 1,
        "company": filters.get("company"),
        "posting_date": ["between", [start_date, end_date]]
    }, ["total_taxes_and_charges"])

    return round(sum(inv.total_taxes_and_charges or 0 for inv in debits), 2)


def get_journal_entries(filters, start_date, end_date):
    total = 0
    entries = frappe.get_all("Journal Entry", {
        "docstatus": 1,
        "custom_is_vat_entry": 1,
        "company": filters.get("company"),
        "posting_date": ["between", [start_date, end_date]]
    })

    for entry in entries:
        accounts = frappe.get_all("Journal Entry Account", {
            "parent": entry.name,
            "custom_entry_type": "Tax Amount"
        }, ["debit_in_account_currency"])

        total += sum(acc.debit_in_account_currency for acc in accounts)

    return round(total, 2)


def get_months():
    today = datetime.date.today()
    current_quarter = (today.month - 1) // 3 + 1

    if current_quarter == 1:
        year = today.year - 1
        start_month = 10
    else:
        year = today.year
        start_month = 3 * (current_quarter - 2) + 1

    months = [start_month + i for i in range(3)]
    month_labels = [calendar.month_abbr[m] for m in months]

    return month_labels, year, months

# import frappe
# from frappe import _
# import calendar
# import datetime

# def execute(filters=None):

#     month_labels, year, months = get_months()

#     columns = get_columns(month_labels)

#     data = get_data(filters, month_labels, months, year)    

#     return columns, data

# def get_columns(month_labels):
#     columns = [
#         {
#             "fieldname": "particulars",
#             "label": _("Particulars"),
#             "fieldtype": "Data",
#             "width": 200,   
#         }
#     ]

#     for month_label in month_labels:
#         columns.append({
#             "fieldname": month_label,
#             "label": _(month_label),
#             "fieldtype": "Currency",
#             "width": 200,
#         })

#     columns.append({
#         "fieldname": "total",
#         "label": _("Total"),
#         "fieldtype": "Currency",
#         "width": 200,
#     })

#     return columns


# def get_data(filters, month_labels, months, year):
#     sales_row = {"particulars": "Sales"}
#     credit_row = {"particulars": "Credit Note (Sales)"}
#     net_sales_row = {"particulars": "Net Sales"}

#     purchase_row = {"particulars": "Purchase"}
#     journal_entry_row = {"particulars": "Purchase (Journal)"}
#     net_purchae_journal_row = {"particulars": "Total Purchase"}
#     purchase_debit_row = {"particulars": "Purchase Debit"}
#     net_purchase_row = {"particulars": "Net Purchase"}
#     net_vat_payable_row = {"particulars": "Net VAT Payable"}

#     total_sales = 0
#     total_credit = 0
#     total_sales_net = 0

#     total_purchase = 0
#     total_journal = 0
#     total_purchase_net = 0  
    
#     total_debit = 0
#     total_purchase_journal = 0
#     total_vat_payable = 0

#     for i, month in enumerate(months):
#         start_date = datetime.date(year, month, 1)
#         end_day = calendar.monthrange(year, month)[1]
#         end_date = datetime.date(year, month, end_day)

#         sales = get_sales(filters, start_date, end_date)
#         sales_row[month_labels[i]] = sales
#         total_sales += sales

#         credit = get_credit(filters, start_date, end_date)
#         credit_row[month_labels[i]] = -credit
#         total_credit += -credit

#         net = sales + credit
#         net = round(net, 2)
#         net_sales_row[month_labels[i]] = net
#         total_sales_net += net

#         purchases = get_purchase(filters, start_date, end_date)
#         purchase_row[month_labels[i]] = purchases
#         total_purchase += purchases 

#         journal_entries = get_journal_entries(filters, start_date, end_date)
#         journal_entry_row[month_labels[i]] = journal_entries
#         total_journal += journal_entries

#         purchase_journal_net = purchases + journal_entries
#         purchase_journal_net = round(purchase_journal_net, 2)
#         net_purchae_journal_row[month_labels[i]] = purchase_journal_net
#         total_purchase_net += purchase_journal_net

#         debit = get_debit(filters, start_date, end_date)
#         purchase_debit_row[month_labels[i]] = -debit
#         total_debit += -debit

#         net_purchase_journal = purchase_journal_net - debit
#         net_purchase_journal = round(net_purchase_journal, 2)
#         net_purchase_row[month_labels[i]] = net_purchase_journal
#         total_purchase_journal += net_purchase_journal

#         net_last = net - net_purchase_journal
#         net_vat_payable_row[month_labels[i]] = net_last
#         total_vat_payable += net_last


#     sales_row["total"] = round(total_sales, 2)
#     credit_row["total"] = round(total_credit, 2)
#     net_sales_row["total"] = round(total_sales_net, 2)
#     purchase_row["total"] = round(total_purchase, 2)
#     journal_entry_row["total"] = round(total_journal, 2)
#     net_purchae_journal_row["total"] = round(total_purchase_net, 2)
#     purchase_debit_row["total"] = round(total_debit, 2)
#     net_purchase_row["total"] = round(total_purchase_journal, 2)
#     net_vat_payable_row["total"] = round(total_vat_payable, 2)


#     return [
#         sales_row, 
#         credit_row, 
#         net_sales_row, 
#         purchase_row, 
#         journal_entry_row, 
#         net_purchae_journal_row,
#         purchase_debit_row,
#         net_purchase_row,
#         net_vat_payable_row
#     ]

# def get_sales(filters, start_date, end_date):
#     sales_invoices = frappe.get_all("Sales Invoice",
#         filters={
#             "docstatus": 1,
#             "is_return": 0,
#             "company": filters.get("company"),
#             "posting_date": ["between", [start_date, end_date]]
#         },
#         fields=["total_taxes_and_charges"]
#     )
    
#     sales = sum(float(inv.total_taxes_and_charges or 0) for inv in sales_invoices)
#     sales = round(sales, 2)

#     return sales

# def get_purchase(filters, start_date, end_date):
#     purchase_invoices = frappe.get_all("Purchase Invoice",
#         filters={
#             "docstatus": 1,
#             "is_return": 0,
#             "company": filters.get("company"),
#             "posting_date": ["between", [start_date, end_date]]
#         },
#         fields=["total_taxes_and_charges"]
#     )
    
#     purchases = sum(float(inv.total_taxes_and_charges or 0) for inv in purchase_invoices)
#     purchases = round(purchases, 2)

#     return purchases

# def get_journal_entries(filters, start_date, end_date):
#     total = 0

#     journal_entries = frappe.get_all("Journal Entry",
#         filters={
#             "docstatus": 1,
#             "custom_is_vat_entry" : 1,
#             "company": filters.get("company"),
#             "posting_date": ["between", [start_date, end_date]]
#         }
#     )

#     for journal_entry in journal_entries:
#         tax_amount = 0
#         accounts = frappe.get_all("Journal Entry Account",
# 			fields=[
# 				"custom_entry_type", 
# 				"debit_in_account_currency", 
# 			],
# 			filters=[
# 				["parent", "=", journal_entry.name],
# 				["custom_entry_type", "in", ["Tax Amount"]],
# 			]
# 		)

#         for journal_entry_account in accounts:
#             if journal_entry_account.custom_entry_type == "Tax Amount":
#                 tax_amount = journal_entry_account.debit_in_account_currency
#         total += tax_amount                

#     return round(total, 2)

# def get_credit(filters, start_date, end_date):    
#     credit_notes = frappe.get_all("Sales Invoice",
#         filters={
#             "docstatus": 1,
#             "is_return": 1,
#             "company": filters.get("company"),
#             "posting_date": ["between", [start_date, end_date]]
#         },
#         fields=["total_taxes_and_charges"]
#     )
#     credit = sum(float(inv.total_taxes_and_charges or 0) for inv in credit_notes)
#     credit = round(credit, 2)

#     return credit

# def get_debit(filters, start_date, end_date):
#     debit_notes = frappe.get_all("Purchase Invoice",
#         filters={
#             "docstatus": 1,
#             "is_return": 1,
#             "company": filters.get("company"),
#             "posting_date": ["between", [start_date, end_date]]
#         },
#         fields=["total_taxes_and_charges"]
#     )        

#     debit = sum(float(inv.total_taxes_and_charges or 0) for inv in debit_notes)
#     debit = round(debit, 2)

#     return debit

# def get_months():
#     today = datetime.date.today()
#     current_quarter = (today.month - 1) // 3 + 1

#     if current_quarter == 1:
#         year = today.year - 1
#         start_month = 10
#     else:
#         year = today.year
#         start_month = 3 * (current_quarter - 2) + 1

#     months = [(start_month + i) for i in range(3)]
#     month_labels = [calendar.month_abbr[m] for m in months]

#     return month_labels, year, months