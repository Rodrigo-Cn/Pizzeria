      document.addEventListener("DOMContentLoaded", function() {
        const editButtons = document.querySelectorAll(".editar-sabor");
        const deleteButtons = document.querySelectorAll(".excluir-sabor");
        const addButtons = document.querySelectorAll(".add-sabor");
      
        const editAlert = document.getElementById("alert-editar");
        const deleteAlert = document.getElementById("alert-excluir");
        const addAlert = document.getElementById("alert-criar");

        function showAlert(alertElement) {
          alertElement.style.display = "block";
        }
      
        editButtons.forEach(button => {
          button.addEventListener("click", function(event) {
            event.preventDefault(); 
            showAlert(editAlert);
          });
        });

        addButtons.forEach(button => {
            button.addEventListener("click", function(event) {
              event.preventDefault(); 
              showAlert(addAlert);
            });
          });
      
        deleteButtons.forEach(button => {
          button.addEventListener("click", function(event) {
            event.preventDefault(); 
            showAlert(deleteAlert);
          });
        });
      });
     