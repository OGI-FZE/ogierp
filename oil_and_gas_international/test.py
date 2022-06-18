from email.mime import base
from typing import final
import frappe 
def testFunc() : 
    all_list = frappe.get_list('Rental Timesheet')
    final_dict = dict()

    for i in all_list : 
        try : 

            take_one = frappe.get_doc('Rental Timesheet' , i['name'])
            take_one_list = take_one.items
            # print(take_one_list)
            for j in take_one_list : 
                base_1 = ''
                days_1 = ''
                assets = (j.assets).split('\n')
                assets.remove('')
                if j.operational_running_check : 
                    # case 1 

                    base_1 = j.base_operational_running
                    days_1 = j.operational_running_days
                elif j.standby_check : 
                    base_1 = j.base_standby
                    days_1 = j.standby_days
                else : 
                    base_1 = j.base_straight
                    days_1 = j.straight_days

                for k in assets : 
                    try : 

                        if final_dict[k] : 
                            final_dict[k].append(base_1 * days_1)
                    except : 
                        final_dict[k] = [base_1 * days_1]


        except : pass     
    print(final_dict)
