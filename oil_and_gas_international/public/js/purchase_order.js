frappe.ui.form.on("Purchase Order", {
   refresh(frm){
       if(frm.doc.docstatus==0){
           console.log('working');
            custom_buttom(frm)
       }
   }
})
const custom_buttom=(frm)=>{
    frm.add_custom_button('Rental Order', () => {
        
    }, 'Get Items From');
    
}