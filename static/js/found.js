$(document).ready(function(){
<!--set the default state-->
	$(".recommend_news").hide();
    $("#you_found").css("color","blue");
	$("#you_like").css("color","black");

<!--set the change if user click "You found" or "You like"-->
    $("#you_found").click(function(){
		$(".found_news").show();
		$(".recommend_news").hide();
		$(this).css("color","blue")
		$("#you_like").css("color","black")
	   });
	
	$("#you_like").click(function(){
		$(".found_news").hide();
		$(".recommend_news").show();
		$(this).css("color","blue")
		$("#you_found").css("color","black")
	   });
	  	   
 });

