import frappe


def create_job_card_against_wo(doc,handller=None):
    work_order = frappe.get_doc("Work Order", doc.work_order)
    for ope in work_order.operations:
        if ope.operation == doc.operation:
            qty_completed = ope.completed_qty
            operation_id = ope.name

            if qty_completed < work_order.qty:
                jc = frappe.new_doc('Job Card')
                jc.update({
                    "company" : doc.company,
                    "work_order" : doc.work_order,
                    "bom_no" : doc.bom_no,
                    "production_item" : doc.production_item,
                    "project" : doc.project,
                    "operation_id": operation_id,
                    "for_quantity" : work_order.qty - qty_completed,
                    "operation" : doc.operation,
                    "workstation" : doc.workstation,
                    "wip_warehouse" : doc.wip_warehouse
                })
                jc.schedule_time_logs(ope)

                jc.insert()
                jc.flags.ignore_mandatory = True