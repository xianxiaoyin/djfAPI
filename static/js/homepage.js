$(document).ready(function(){

    $("#search_btn").click(function() {
	
       var isInputEmpty = $("#input_bar").val()?false:true;
	   
	   if(isInputEmpty == true)
	   {
	      alert("Your input can't be empty.");
		  $("#input_form").attr("action","index.html");
	   }
	   
	   else if( $("#input_bar").val()<0 ||$("#input_bar").val()>9999)
	   {
	     alert("Your input should be chosen from 0 to 9999,Please input again.");
		 $("#input_form").attr("action","index.html");
	   }
	   else
	   {
	     
	   }	   
    });  
 });

