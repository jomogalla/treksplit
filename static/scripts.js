$(document).ready(function(){
// $('body').addClass('animated fadeIn');

//initialize Masonry
var $container = $('#expense_area');
$container.masonry({
  columnWidth: 420,
  itemSelector: '.expense'
});
// Hiding things that only work in chrome
if(!Boolean(window.chrome)){
	$("<style type='text/css'> .color{ display:none;} </style>").appendTo("head");
	$('#deadline_toggle').parent().css('display', 'none');
}


//******************************** CSRF Stuff ********************************//
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Binding Tipsy Stuff
// $('.finalize').tipsy({gravity: 'n'});
// $('.add').tipsy({gravity: 'n'});
// $('.edit').tipsy({gravity: 'nw'});
// $('#group_title').tipsy({gravity: 'e'});


//******************************** Expense Functions ********************************//

// Add Expense
// Should this be solely on a click event?
$( "#expense_area" ).on( "click", ".expense_button.add", function(){
	$(this).focus();
});
// triggered by focusing on the Add Button
$( "#expense_area" ).on( "focus", ".expense_button.add", function(){
	var persons_id = $(this).closest(".expense").data("person");


	// I would like to get this from the server so I don't have two parallel sets of Expense Rows
	//  that always need updating, it just isnt quick enough for the interface to do that..
	var new_row = $('<tr class="row"{% if expense.id %} data-expense="{{expense.id}}"{% endif %}{% if person.id %} data-owner="{{person.id}}"{% endif %}><td><button class="expense_button delete" title="delete the expense"><i class="fa fa-times"></i></button></td><td class="item_name"><input type="text" placeholder="item" title="edit the expense\'s name"{% if expense.name %}value="{{expense.name}}"{% endif %}></td><td class="cost"><input type="number" title="edit the expense\'s price"placeholder="price" {% if expense.price %}value="{{expense.price}}"{% endif %}></td><!-- <td><button class="expense_button comment" title="comment on this expense"><i class="fa fa-comment"></i></button></td> --></tr>');

	// first expense added has no row to grab
	// $('#' + persons_id +' table tr:last').after(new_row);
	$('#' + persons_id +' table tbody').append(new_row);
	new_row.attr('data-owner', persons_id);
	new_row.addClass("new_row");
	// $(this).closest(".expense").toggleClass('maximum_z_index');
	$('.new_row').show("slow", function(){$container.masonry();});
	// setTimeout(function(){$(this).closest(".expense").toggleClass('maximum_z_index');}, 500);


	$('.new_row').removeClass("new_row");

	// focus the cursor in the created input box
	$(this).parent().siblings(".expense_table").find('tr:last-child .item_name input').focus();

	
	// alert(persons_id);
	// add the expense to the database
	$.ajax({
	    url: '/expense/0/',
	    type: 'POST',
	    data: {
	    	owner: persons_id,
	    },
	    success: function(result) {
	    	// alert(new_row.html());
	   	     display_update('expense ' + result + ' successfully added');
	   	     // ALSO, UPDATE THE above added html's id!!!
	   	     // new_expense_id = result;
	   	     // alert(new_row.parent().html());
	   	     // alert($("#" + random_identifier));
	   	     new_row.attr('data-expense', result); 

			// $('.new_row').removeClass("new_row");
	    }
	});

});


// Delete expense
$( "#expense_area" ).on( "click", ".expense_button.delete", function() {
	var expense_button = $(this);
	var expense_id = $(this).closest('tr').data("expense");
	$(this).closest('tr td input').addClass('deleting');
	$.ajax({
	    url: '/expense/' + expense_id + '/',
	    type: 'POST',
	    data: {
	    	operation: 'delete',
	    },
	    success: function(result) {
	   	  	expense_button.closest("tr").hide('fast', function(){
				expense_button.closest("tr").remove();
				$container.masonry();
				update_numbers();
			});
			display_update('expense ' + expense_id + ' successfully deleted');			
	    }
	});
});


// Change Expense's Name
$("#expense_area").on("change", ".item_name input",function(){
	// if the expense id does not exist, set timeout and try again
	var owner = $(this);
	var expenses_id = $(this).closest("tr").data("expense");
	owner.addClass('updating');
	$.ajax({
	    url: '/expense/' + expenses_id + "/",
	    type: 'POST',
	    data: {
	    	operation: "change_name",
	    	name: $(this).val(),
	    },
	    success: function(result) {
	   	    display_update('expense ' + result + "\'s name successfully changed");		
	   	    owner.removeClass('updating');	
	    }
	});
});


// Change Expense's Price
$("#expense_area").on("change", ".cost input",function(){
	// if the expense id does not exist, set timeout and try again
	var owner = $(this);
	owner.addClass('updating');
	var expenses_id = $(this).closest("tr").data("expense");
	
	$.ajax({
	    url: '/expense/' + expenses_id + "/",
	    type: 'POST',
	    data: {
	    	operation: "change_price",
	    	price: $(this).val(),
	    },
	    success: function(result) {
	   	    display_update('expense ' + result + "\'s price successfully changed");	
	   	    owner.removeClass('updating');		
	    }
	});
});

//******************************** Person Functions ********************************//

// Add Person
$('#add_user').click(function(){
	$('#add_user button').text('adding person...');
	var group_id = $('#group_name').data("group");
	$.ajax({
	    url: '/person/0/',
	    type: 'POST',
	    data: {
	    	group: group_id,
	    },
	    success: function(result) {
   	     	$('#add_user').before(result);

   	     	// Grab their ID
   	     	// var persons_id = $('#add_user').prev().find('.expense').attr("data", "person");
   	     	// var persons_color = $('#add_user').prev().find('.expense').attr("color");
   	     	// if(typeof $('#add_user').prev().find('.expense').data("person") != null){
   	     	// 	var persons_id = $('#add_user').prev().find('.expense').attr("data", "person");
   	     	// }
   	     	// else{
   	     	// 	var persons_id = 
   	     	// }
   	     	var persons_id = $('#add_user').prev().data("person");
   	     	var persons_color = $('#add_user').prev().data("color");
   	     	$('#'+persons_id).addClass('new_row');


   	     	// Animate it all nicely
			$('#' + persons_id).slideToggle("slow");
			$('#' + persons_id).removeClass('new_row');
			// $('#' + persons_id).css('color', 'new_row');

			// Let them know whats happening
			display_update("person " + persons_id + " created");

			// Add them to the sidebar
			$('#average_row').before('<tr class="sidebar_person_total new_row" id="sidebar_person_total_' + persons_id + '"><td class="person_name" style="color:' + persons_color +';">-----</td><td class="align_right"> 0.00 </td><td class="align_right">0.00</td></tr>');

			$('#sidebar_person_total_' + persons_id).show("slow");
			$('#sidebar_person_total_' + persons_id).removeClass('new_row');
			$('#sidebar_person_total_' + persons_id + ':first-child').css('color', '#' + persons_color);

			// add them into masonry
			var new_expense = $('#' + persons_id);
			$container.append( new_expense ).masonry( 'appended', new_expense );
			$container.masonry();
			setTimeout(function(){$container.masonry();}, 500);

			// // swap back the add user button text
			$('#add_user button').text('add another person');
			update_numbers();
	    }
	});
});


// Delete Person
$( "#expense_area" ).on( "click", ".delete_person", function(){
	var persons_name = $(this).closest(".expense").data("name");
	var persons_id = $(this).closest(".expense").data("person");

	if(typeof persons_name == "undefined"){
		persons_name = "person " + persons_id;
	}

	blackout_prompt("delete " + persons_name + "?").then(function(delete_confirmation){
		if(delete_confirmation == true){
			$("#centered").css("display","block");
			$("#centered").html("<i class='fa fa-cog fa-spin fa-5x'></i><p>deleting " + persons_name + "</p>");
			$("#blackout").css("display","block");
			$.ajax({
			    url: '/person/' + persons_id + "/",
			    type: 'POST',
			    data: {
			    	operation: "delete",
			    },
			    success: function(result) {
	   	     		//remove the person	
			   	    display_update(persons_name + ' successfully deleted');	
	
					// remove clicked element
					// msnry.remove( $('#'+result).closest('.expense'));
				  	// layout remaining item elements
					// msnry.reload();
					$('#'+result).closest('.expense').remove();
					$('#sidebar_person_total_'+ result).remove();
					$("#centered").css("display","none");
					$("#blackout").css("display","none");
					$container.masonry()
					update_numbers();

			    }
			});
		}
	});
});


// Toggle Edit Person slider
$( "#expense_area" ).on( "click", ".expense_button.edit", function(){
	$(this).parent().next('.edit_person_wrapper').slideToggle( "fast", function(){$container.masonry()});
});


// Change Person's Name
$( "#expense_area" ).on( "change", ".expense_owner input", function(){
	var owner = $(this);
	var persons_id = $(this).closest(".expense").data("person");
	var persons_old_name = $(this).closest(".expense").attr("data-name");
	var persons_new_name = $(this).val();
	if(typeof persons__old_name == "undefined"){
		persons_old_name = "person " + persons_id;
	}

	
	$(this).addClass('updating');
	$.ajax({
	    url: '/person/' + persons_id + "/",
	    type: 'POST',
	    data: {
	    	operation: "change_name",
	    	name: persons_new_name,
	    },
	    success: function(result) {
	    	// below code aimt working
	    	if(typeof persons_old_name == undefined){
				display_update(persons_new_name + "\'s name added");
			}
	   	    display_update(persons_old_name + "\'s name changed to " + persons_new_name);	
	   	    $('#' + persons_id).data("name", persons_new_name);
	   	    $('#' + persons_id).attr("data-name", persons_new_name);
	   	    $(owner).removeClass('updating');
	   	    update_numbers();
	    }
	});
});


// Change Person's Color
$( "#expense_area" ).on( "change", ".color", function(){
	// Grab the owners ID
	var persons_id = $(this).closest(".expense").data("person");
	var persons_name = $(this).closest(".expense").data("name");

	// Swap out the header color
	$(this).closest(".expense").find(".expense_header").css("background-color", $(this).val());

	// Swap out their sidebar color
	$('#sidebar_person_total_' + persons_id + " .person_name").css("color", $(this).val());

	// Update the persons color data
	$(this).closest(".expense").attr("data-color", $(this).val());

	$.ajax({
	    url: '/person/' + persons_id + "/",
	    type: 'POST',
	    data: {
	    	operation: "change_color",
	    	color: $(this).val(),
	    },
	    success: function(result) {
	   	    display_update(persons_name + "\'s color changed");			
	    }
	});
});

// finalize persons expenses
$( "#expense_area" ).on( "click", ".finalize", function(){
	// Grab the owners ID
	var button = $(this);
	var persons_id = $(this).closest(".expense").data("person");
	var persons_name = $(this).closest(".expense").data("name");
	if(typeof persons_name == "undefined"){
		persons_name = "Person " + persons_id;
	}

	// If were finalized, unfinalize
	if (button.hasClass('finalized')){
		$.ajax({
		    url: '/person/' + persons_id + "/",
		    type: 'POST',
		    data: {
		    	operation: "unfinalize",
		    },
		    success: function(result) {
		   	    display_update(persons_name + "\'s expenses are not done");
		   	    button.toggleClass('finalized');			
		    }
		});
	}
	// Else finalize that shit
	else{
		$.ajax({
		    url: '/person/' + persons_id + "/",
		    type: 'POST',
		    data: {
		    	operation: "finalize",
		    },
		    success: function(result) {
		   	    display_update(persons_name + "\'s expenses are all done");
		   	    button.toggleClass('finalized');			
		    }
		});
	}
});


// Change Person's Email
$("#expense_area").on("change", ".email",function(){

	var persons_id = $(this).closest(".expense").data("person");
	var persons_name = $(this).closest(".expense").data("name");
	$.ajax({
	    url: '/person/' + persons_id + "/",
	    type: 'POST',
	    data: {
	    	operation: "change_email",
	    	email: $(this).val(),
	    },
	    success: function(result) {
	   	    display_update(persons_name + "\'s email changed");			
	    },
	    error: function(){
	    	display_update('is that a real email?');
	    }
	});
});
// Make the placeholder disappear when focused on
$("#expense_area").on("focus", ".email",function(){
	$(this).attr("placeholder", "");
});

$("#expense_area").on("blur", ".email",function(){
	$(this).attr("placeholder", "add person's email");
});


// Change Person's Passcode - UNUSED
$("#expense_area").on("change", ".password",function(){
	display_update('functionality not implemented');
});
$("#expense_area").on("change", ".confirm_password",function(){
	display_update('functionality not implemented');
});



//******************************** Group Functions ********************************//

// Add Group
// currently unused
$( "#expense_area" ).on( "click", "#add_group", function() {
	// Dump this person from the tables VIA AJAX
	$("#centered").text("TREK/SPLIT");
	$("#centered").addClass("centered_text");



	$.ajax({
	    url: '/group/0/',
	    type: 'POST',
	    data: {},
	    success: function(result) {
	   	     // put the code below in here plz
	   	     // alert(result);
	   	     window.location.replace("./" + result);
	    }
	});
});

// Delete Group
$("#right_info_bar").on("click", "#delete_group",function(){

	var group_id = $("#group_name").data('group');
	var group_name = $('#group_name').data('name');
          				

	if(typeof group_name == "undefined"){
		group_name = "group " + group_id;
	}

	//prompt them to make sure they wanna do it
	blackout_prompt("delete " + group_name + "?").then(function(delete_confirmation){
		if(delete_confirmation == true){
			$("#centered").css("display","block");
			$("#centered").html("<i class='fa fa-cog fa-spin fa-5x'></i><p>deleting " + group_name + "</p>");
			$("#blackout").css("display","block");
			$.ajax({
			    url: '/group/' + group_id + "/",
			    type: 'POST',
			    data: {
			    	operation: "delete",
			    },
			    success: function(result) {
			    	var time_to_redirect = 1000;
			  		$('body').addClass('animated fadeOut');
			  		setTimeout(function(){
			  			window.location.replace("/");
			  		}, time_to_redirect);
			    }
			});
		}
	});
	

});

// Change group title
$('#group_title').change(function(){
	var their_new_name = $(this).val();
	// Using django to generate the below?
	// bad/good?
	var the_input_box = $(this);
	var group_id = $("#group_name").data("group");

	$.ajax({
	    url: '/group/' + group_id + '/',
	    type: 'POST',
	    data: {
	    	operation: 'change_name',
	    	name: their_new_name,
	    },
	    success: function(result) {
	    	if(result != ""){
		   	     display_update('group name changed to ' + result);
		   	     $(document).attr('title', 'trek/split - ' +result);
		   	     the_input_box.data("name", result);
		   	     // $("#group_name").text(result);
		   	     $("#group_name").attr("data-name", result);

		   	 }
		   	 else{
		   	 	display_update('group name removed');
				$(document).attr('title', 'trek/split');
				the_input_box.data("name", "");
				// $("#group_name").text(group_id);
				$("#group_name").attr("data-name", "");	
		   	 }
	    }
	});
});
$('#group_title').focus(function(){
	$(this).attr("placeholder", "");
});

$('#group_title').blur(function(){
	$(this).attr("placeholder", "add group name");
});

// Send Invitation Email

// code for making the email input pretty/seamless
$('#invite_email').focus(function(){
	$(this).attr("placeholder", "");
});

$('#invite_email').blur(function(){
	$(this).attr("placeholder", "share by email");
});

$('#invite_email').keypress(function(e) {
    if(e.which == 13) {
       $('#send_email').click();
    }
});

// actually send the email now
$('#send_email').click(function(){
	var email_to_invite = $('#invite_email').val();
	// check to see if they even put anything
	if (email_to_invite == ''){
		display_update("that isn\'t an email address");
		return false;
	}
	var send_button = $(this);
	var group_id = $("#group_name").data("group");
	var button_text = send_button.html();
	send_button.html("send <i class='fa fa-cog fa-spin'></i>");

	$.ajax({
	    url: '/group/' + group_id + '/',
	    type: 'POST',
	    data: {
	    	operation: 'send_invitation',
	    	email: email_to_invite,
	    },
	    success: function(result) {
	    	display_update(result);
	    	$('#invite_email').val("");
	    	send_button.html(button_text);

	    },
	    error: function(){
	    	display_update('email failed to send');
	    	send_button.html(button_text);
	    }
	});
});

// Toggle Settings Tab
$('#settings_button').click( function(){
	// If the share tab is open, close it first
	if($('#share').css('display') == 'block'){
		border_swap('#settings_button', '#share_button');
		$( "#share" ).slideToggle( "fast");
		$( "#settings" ).slideToggle( "fast");
	}
	// If the about tab is open, close it first
	else if($('#help_button').hasClass('selected_button')){
		border_swap('#settings_button', '#help_button');
		$( ".help_box" ).slideToggle( "fast");
		$('#add_user').toggleClass('adduser_help_offset');
		$( "#settings" ).slideToggle( "fast");
	}
	else{
		border_swap('#settings_button', '#settings_button');
		$( "#settings" ).slideToggle( "fast");

	}

    // Animation complete.
});

// Toggle Share Tab
$('#share_button').click(function(){
	//if settings is open, we gotta fade it out too
	if($('#settings').css('display') == 'block'){
		border_swap('#share_button', '#settings_button');
		$( "#settings" ).slideToggle( "fast");
		$( "#share" ).slideToggle( "fast");
	}
	//if help is open, we gotta close it
	else if ($('#help_button').hasClass('selected_button')){
		border_swap('#share_button', '#help_button');
		$('.help_box').slideToggle("fast", function(){$container.masonry()});
		$('#add_user').toggleClass('adduser_help_offset');
		$('#expense_area').toggleClass('expense_area_help_offset');
		$( "#share" ).slideToggle( "fast");
	}
	else{
		border_swap('#share_button', '#share_button');
		$( "#share" ).slideToggle( "fast");
	}
	// Below focuses on the email input
	// $("#invite_email").focus();
});

// Still in here because it has been recently removed/changed
// Toggle About Tab
// $('#about_button').click(function(){
// 	//if settings is open, we gotta fade it out too
// 	if($('#settings').css('display') == 'block'){
// 		border_swap('#about_button', '#settings_button');
// 		$( "#settings" ).slideToggle( "fast");
// 		$( "#about" ).slideToggle( "fast");
		
// 	}
// 	//if share is open, we gotta close it
// 	else if($('#share').css('display') == 'block'){
// 		border_swap('#about_button', '#share_button');
// 		$( "#share" ).slideToggle( "fast");
// 		$( "#about" ).slideToggle( "fast");
// 	}
// 	else{
// 		border_swap('#about_button', '#about_button');
// 		$( '#about' ).slideToggle( "fast");

// 	}
// });
// Toggle Help
$('#help_button').click(function(){
	//if settings is open, we gotta fade it out too
	if($('#settings').css('display') == 'block'){
		border_swap('#help_button', '#settings_button');
		$( "#settings" ).slideToggle( "fast");
		$('.help_box').slideToggle("fast", function(){$container.masonry()});
		$('#add_user').toggleClass('adduser_help_offset');
		$('#expense_area').toggleClass('expense_area_help_offset');
		
	}
	//if share is open, we gotta close it
	else if($('#share').css('display') == 'block'){
		border_swap('#help_button', '#share_button');
		$( "#share" ).slideToggle( "fast");
		$('.help_box').slideToggle("fast", function(){$container.masonry()});
		$('#add_user').toggleClass('adduser_help_offset');
		$('#expense_area').toggleClass('expense_area_help_offset');
	}
	else{
		border_swap('#help_button', '#help_button');
		$('.help_box').slideToggle("fast", function(){$container.masonry()});
		$('#add_user').toggleClass('adduser_help_offset');
		$('#expense_area').toggleClass('expense_area_help_offset');


	}
});

// Change the Group's expense options
// NOT IMPLEMENTED

// Toggle Editable Deadline
$('#deadline_toggle').click(function(){
	$(this).hide();
	$('#change_group_deadline').show();
	$('#change_group_deadline').focus();
});

//get that button back ^
$('#change_group_deadline').blur(function(){
	$(this).hide();
	$('#deadline_toggle').show();
});

// Change Group Deadline
$('#change_group_deadline').change(function(){
	var new_deadline = $(this).val(); 
	var group_id = $("#group_name").data("group");

	$.ajax({
	    url: '/group/' + group_id + '/',
	    type: 'POST',
	    data: {
	    	operation: 'change_deadline',
	    	deadline: new_deadline,
	    },
	    success: function(result) {
	    	display_update("deadline changed to " + new_deadline);
	    	$('#deadline_toggle').text('change deadline');
	    },
	});

});

// Change Group Passcode
$('#change_group_passcode_confirm').keypress(function(e) {
	// IF data-passcode == yes, require them to input the current passcode < potentially insecure
	var group_id = $("#group_name").data("group");
	if(e.which == 13 || e.which == 9){
		var first_passcode = $('#change_group_passcode').val();
		var second_passcode = $('#change_group_passcode_confirm').val();
		if(first_passcode == second_passcode){
				$(this).val("");
				$('#change_group_passcode').val("");
				$(this).attr("placeholder", "updating passcode");		
				$.ajax({
				    url: '/group/' + group_id + '/',
				    type: 'POST',
				    data: {
				    	operation: 'change_passcode',
				    	passcode: first_passcode,
				    },
				    success: function(result) {
				    	$('#change_group_passcode_confirm').css('display', 'none');
				    	$('#change_group_passcode').css('display', 'inline-block');
				    	$('#change_group_passcode_confirm').attr("placeholder","confirm passcode");
				    	$('#change_group_passcode').attr("placeholder","change group passcode");
				    	$('#change_group_passcode').blur();
				    	display_update(result);
				    },
				});
		}
		else{
			$(this).css('display', 'none');
			$(this).val("");
			$('#change_group_passcode').val("");
			$('#change_group_passcode').attr("placeholder", "try again...");
			$('#change_group_passcode').css('display', 'inline-block');
			$('#change_group_passcode').focus();
		}
	}
});

// If the user presses enter or tab while using the group passcode block,
// hide the current passcode input, and display the confirmation
$('#change_group_passcode').keypress(function(e) {
	if(e.which == 13 || e.which == 9){
		$(this).css('display', 'none');
		$('#change_group_passcode_confirm').css('display', 'inline-block');
		$('#change_group_passcode_confirm').focus();
			
	}
});
// Make the placeholder disappear when focused on
$('#change_group_passcode').focus(function(){
	$(this).attr("placeholder", "");
});

$('#change_group_passcode').blur(function(){
	$(this).attr("placeholder", "change group passcode");
});


// // Toggle Requirement for individual Passcodes
// $("#right_info_bar").on("click", "#change_passcode_requirement",function(){
// 	display_update('functionality not implemented');
// });


// Hide the advertisement... display update for now, and the buttons not even here
$("#hide_ad").click(function(){
	$('#advertisement').slideToggle("slow");
});





//******************************** General Functions ********************************//

// hide or display the control bar for mobile users
$(function(){
  $('#right_control_bar').data('size','big');
}); 
$(window).scroll(function(){	
	if($(window).width() < 1024){
		if($(window).scrollTop() > 20){
			if($('#right_control_bar').data('size') == 'big'){
				$('#right_control_bar').data('size','small');
				$('#right_control_bar').stop().animate({bottom: "-225px"});
			}
		}
		else{
			if($('#right_control_bar').data('size') == 'small'){
				$('#right_control_bar').data('size','big');
				$('#right_control_bar').stop().animate({bottom: "0px"});
			}

		}
	}
	else{
		if($('#right_control_bar').data('size') == 'small'){
				$('#right_control_bar').data('size','big');
				$('#right_control_bar').stop().animate({bottom: "0px"});
		}
	}
});

// Update all the information on input change
$( "#expense_area" ).on( "change", "input", function(){
	update_numbers();
});

// Close the warning dialog 
$('#close_warning').click(function(){
	$('#warning').hide();
});

// The Yes/No Prompt code for deleting things
var blackout_prompt = function(prompt){
	$('#centered').css("display", "block");
	$('#blackout').css("display","block");
	$('#centered').html("<p>" + prompt + "</p><button id='yes' class='text_button modal'>yes</button> / <button id='no' class='text_button modal'>no</button>");
	// var response = false;
	var deferred = $.Deferred();
	$('#yes').click(function(){
		deferred.resolve(true);
	});
	$('#no').click(function(){
		deferred.resolve(false);
		$('#centered').css("display", "none");
		$('#blackout').css("display","none");
	});
	return deferred.promise();
};
// >> ?? <<
var confimation = function(){
	
};

// Code used to underline the current control bar button (help/share/settings)
var border_swap = function(id_on, id_off){
	if(id_on == id_off){
		if($(id_on).hasClass('selected_button')){
			$(id_on).removeClass('selected_button');
		}
		else{
			$(id_on).addClass('selected_button');
		}
	}
	else{
		$(id_off).removeClass('selected_button');
		$(id_on).addClass('selected_button');		
	}
};

// dumb name... code for updating the update_display 
var display_update = function( message ){
	var old_text = $('#update_display').html();

	// add the text sent to the div
	$('#update_display').html(old_text + "<div class='update_line'>" + message + "</div>");

	// if we have more lines than max_update_length, remove the top lines
	var max_update_length = 5;
	if($('.update_line').length > max_update_length){
		var num_to_remove = $('.update_line').length - max_update_length;
		$('.update_line:lt(' + num_to_remove +')').remove();
	}

};

// THE BREAD & BUTTER - this updates everything on screen 
// & calculates payments 
var update_numbers = function(){
	// running question:
	// Do I do this in jquery? Is that more vulnerable to people fucking around?
	// it will mean less data transfer, maybe quicker UI?
	// or do I do it server side and just return everything?
	// do it server side so i can email ppl the tables

	// UPDATES EACH PERSONS TOTAL
	var numberRegex = /^[+-]?\d+(\.\d+)?([eE][+-]?\d+)?$/;
	$('.expense').each(function(){
		// UPDATES EACH PERSONS TOTAL
		var personal_sum = 0;
		$(this).find('td.cost input').each(function(){
			// make sure our value is a number and there is something there
			if(numberRegex.test($(this).val()) && $(this).val() != "") {
	  			personal_sum += parseFloat($(this).val()); 
	  			// FIGURE OUT HOW TO ROUND THESE DAMN NUMBERS
	  			// $(this).val(parseFloat($(this).val()));
			}
		    
		});  
		// replace the total
		$(this).children('.expense_header').children('.expense_total').text(personal_sum.toFixed(2));

		// UPDATES TOTALS ON THE SIDEBAR
		$('#sidebar_person_total_' + $(this).attr('id')).children('td:last').text(personal_sum.toFixed(2));

	});

	

	//UPDATES THE GROUPS AVERAGE AND TOTAL FIELDS
	var sum = 0,
		num_expenses = 0;
	$('.expense_total').each(function(){
	    sum += parseFloat($(this).text());  
	    num_expenses++;
	});
	if(num_expenses != 0){
		var average = (sum/num_expenses).toFixed(2);
	}
	else{
		var average = "--.--";
	}
	$("#total").text("$ " + sum.toFixed(2));
	$("#average").text(average);


	$('.expense').each(function(){
		var difference_td = $('#sidebar_person_total_' + $(this).attr('id')).children('td:nth-last-child(2)');
		var total_td = $('#sidebar_person_total_' + $(this).attr('id')).children('td:last');

		var difference = parseFloat(total_td.text())-average;

		difference_td.text(difference.toFixed(2));

		// making the difference prettier (red/black/negatives/positives/etc)
		if(difference<0){
			if(!difference_td.hasClass('negative_amount')){
				difference_td.addClass('negative_amount');
				difference_td.removeClass('positive_amount');
			}
		}
		else if(difference>0){
			difference_td.addClass('positive_amount');
			if(difference_td.hasClass('negative_amount')){
				difference_td.removeClass('negative_amount');
			}			
		}
		else{
			difference_td.removeClass('positive_amount');
			difference_td.removeClass('negative_amount');
			difference_td.text('-----');
		}

	});

	// UPDATES THE NAMES
	$('.expense').each(function(){
		var name = $(this).find('.expense_owner input').val();

		if(name.length == 0){
			$('#sidebar_person_total_' + $(this).attr('id')).children('td:first').text('-----');	
		}
		else{
			$('#sidebar_person_total_' + $(this).attr('id')).children('td:first').text(name);
		}

		
	});

	// Calculate the payment plan
	var people = [];
	// Person = [Name, Amount, Color]
	var person = [];
	$('.expense').each(function(){

		var name = $(this).attr('data-name');
		if(typeof name == "undefined"){
			name = '-----';
		}
		var expenses = $(this).children('.expense_header').children('.expense_total').text();
		var color = $(this).attr('data-color');
		person = [name, expenses, color];
		people.push(person);
	});

	var number_of_people = people.length;

	var lenders = [];
	var debtors = [];

	// Transaction = [debtor, lender, amount, debtor color, lender color]
	var transaction = [];
	var transactions = [];

	while(people.length > 0){
		person = people.pop();
		// grabbing the debtors
		if (parseFloat(person[1]) < average){
			person[1] = average - parseFloat(person[1]);
			debtors.push(person);
		}
		// grabbing the lenders
		else if(parseFloat(person[1]) > average){
			person[1] = parseFloat(person[1]) - average;
			lenders.push(person);
		}
		// If they paid the average, they disappear here :O
	}

	while(lenders.length > 0 && debtors.length > 0){
		for(var i = 0; i < debtors.length; i++){
			for(var j = 0; j < lenders.length; j++){
				if(debtors[i][1] == lenders[j][1]){
					transaction = [debtors[i][0], lenders[j][0], debtors[i][1], debtors[i][2], lenders[j][2]];
					transactions.push(transaction);
					lenders.splice(j, 1);
					debtors.splice(i, 1);
					continue;
				}
			}
		}
		if(debtors.length > 0 && lenders.length > 0){
			var debtor = debtors.pop();
			var lender = lenders.pop();
			if(debtor[1] < lender[1]){
				transaction = [debtor[0], lender[0], debtor[1], debtor[2], lender[2]];
				transactions.push(transaction);
				lender[1] = lender[1] - debtor[1];
				lenders.push(lender);
			}
			else{
				transaction = [debtor[0], lender[0], lender[1], debtor[2], lender[2]];
				transactions.push(transaction);
				debtor[1] = debtor[1] - lender[1];
				debtors.push(debtor);
			}
		}
	}
	// reversing transactions for some easy popping action
	transactions.reverse();

	// Go through and populate the payment table with what we just calculated
	$('#payment_table').html('');
	while(transactions.length > 0){
		transaction = transactions.pop();
		var pretty_payment = '<tr><td style="color:'+ transaction[3]+';">' + transaction[0] +'</td><td class="owes">owes</td><td style="color:'+ transaction[4]+';">'+ transaction[1] +'</td><td class="align_center">' + transaction[2].toFixed(2) + '</td></tr>';
		$('#payment_table').append(pretty_payment);
	}
};
update_numbers();
});