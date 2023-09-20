# Copyright (c) 2022, . and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from erpnext.accounts.report.financial_statements import get_period_list


def execute(filters=None):
    period_list = get_period_list(
        from_fiscal_year = filters.fiscal_year,
        to_fiscal_year = filters.fiscal_year,
        period_start_date = filters.from_date,
        period_end_date = filters.to_date,
        periodicity = 'Monthly',
        filter_based_on = "Fiscal Year",
        company=filters.company,
    )

    columns, data = get_columns(filters, period_list), get_data(filters, period_list)
    return columns, data
    
def get_columns(filters, period_list):
    columns = [
    {'label':_('Employee Name'),'field_name':'employee_name','width':220,'fieldtype':'Data'},
    {'label':_('Designation'),'field_name':'designation','width':220,'fieldtype':'Data'},
    {'label' : _('Count'),'field_name' : 'count','fieldtype' : 'Int'},
    ]

    for period in period_list:
        columns.append(
            {
                "fieldname": period.key,
                "label": period.label,
                "fieldtype": "Currency" ,
                "width": 130 ,
                "align": "right",

            })

    return columns


def get_data(filters, period_list):
    sql_data = []
    conditions = ""
    staf_conditions = ""
    if filters.get('company'):
        conditions += " where e.company = '{}'".format(filters.get('company'))
        staf_conditions += " and sp.company = '{}'".format(filters.get('company'))
    sql_data = frappe.db.sql("""select e.employee_name,e.employee, e.company, e.designation,e.department,ss.base,EXTRACT(MONTH FROM ss.from_date) as month,EXTRACT(YEAR FROM ss.from_date) as year from `tabEmployee` e 
                            left join (select base,employee,from_date from `tabSalary Structure Assignment`) as ss on ss.employee = e.employee %s""" %(conditions), as_dict = 1)
    staffing_plan = frappe.db.sql("""select spd.designation, spd.number_of_positions - spd.already_hired as count,
                                     sp.department,spd.estimated_cost_per_position as base, EXTRACT(MONTH from sp.from_date) as month, EXTRACT(YEAR from sp.from_date) as year
                                    from `tabStaffing Plan Detail` spd
                                    left join (select name,department,docstatus,from_date,company from
                                    `tabStaffing Plan`) as sp on sp.name = spd.parent where sp.docstatus = 1 %s """ %(staf_conditions), as_dict=1)
    print('\n \n')
    for s in staffing_plan:
        s['employee_name'] = ""
        s['date'] = "/".join([str(s['month']),str(s['year'])])
        sql_data.append(s)

    data = {}
    for i in sql_data:
        employee_name = i['employee_name']
        designation = i['designation']
        if not "count" in i.keys():
            count = 1
        data.setdefault(i['department'], []).append(i)

    result = []	
    if data:	
        
        for d in data:
            sub_total = 0
            result.append({'employee_name':d,'designation':'','count':0,'indent':0})
    
            for i in data[d]:
                if i['employee_name']:
                    i['count'] = 1
                    i['date'] = "/".join([str(i['month']),str(i['year'])])
                sub_total += i['count']
                i['indent'] = 1
                if i['employee_name']:
                    i['count'] = 1
                result.append(i)
            result.append({'employee_name':'','designation':'Sub Total','count':sub_total,"bold":1})

    total = 0	
    t = 0
    result_without_department = []
    total_row = {}
    for record in result:
        if record['designation'] == 'Sub Total':
            total += record['count']
        
        number_to_month =  {'1':'jan','2':'feb','3':'mar','4':'apr','5':'may','6':'jun','7':'jul',
                            '8':'aug','9':'sep','10':'oct','11':'nov','12':'dec'}
        if 'date' in record.keys():
            mon = record['date'].split("/")[0]
            year = record['date'].split("/")[1]
            if 'employee' in record.keys():
                if frappe.db.exists("Salary Structure Assignment",{'employee':record['employee']}):
                    if int(year) == int(filters.get("fiscal_year")):
                        for d in range(int(mon),13):
                            month_fiscal = number_to_month[str(d)] + "_" + filters.get("fiscal_year")
                            record[month_fiscal] = record['base']
                    elif int(year) <= int(filters.get("fiscal_year")):
                        for d in range(1,13):
                            month_fiscal = number_to_month[str(d)] + "_" + filters.get("fiscal_year")
                            record[month_fiscal] = record['base']
            else:
                    if int(year) == int(filters.get("fiscal_year")):
                        for d in range(int(mon),13):
                            month_fiscal = number_to_month[str(d)] + "_" + filters.get("fiscal_year")
                            record[month_fiscal] = record['base']*record['count']
                    elif int(year) <= int(filters.get("fiscal_year")):
                        for d in range(1,13):
                            month_fiscal = number_to_month[str(d)] + "_" + filters.get("fiscal_year")
                            record[month_fiscal] = record['base']*record['count']
        if record['designation'] not in ['Sub Total','']:
            result_without_department.append(record)
    import collections
    total_per_month = collections.Counter()
    for r in result_without_department:
        total_per_month.update(r)
    for k in dict(total_per_month).keys():
        if "_2" in k:
            total_row[k] = dict(total_per_month)[k]
    print(total_row)
    total_row['designation'] = "Total"
    total_row['count'] = total
    total_row['bold'] = 1
    result.append(total_row)
    return result




    