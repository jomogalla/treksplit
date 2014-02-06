$(document).ready(function(){
// RUNNING QUESTION
// on the edit/settings boxes, do I have an edit toggle then do the updates in there?
// or what? that doesnt make sense...have headache
// ok...each button/functionality has a function...


// also wondering about using all these tds, and tree traversals
// seems like a very fragile system, where one small html change will fuck everything
// 
// ****BUGS****
// > problem:
// Create new user form is not editable
// > reason:
// the buttons are not bound to events as they are added after jquery initializes all its bindings
// > problem:
// expense totals are not updating on row delete, only after second row delete
// > reason:
// no clue

$('body').addClass('animated fadeIn');
//

//   var $container = $('#expense_area');
// // initialize
// $container.masonry({
// 	columnWidth: 440,
// 	itemSelector: '.expense_wrapper',
// 	isAnimated: true,
// });
// var msnry = $container.data('masonry');
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


//******************************** Expense Functions ********************************//

// Add Expense
// triggered by focusing on the Add Button
$( "#expense_area" ).on( "focus", ".expense_button.add", function(){
	var persons_id = $(this).closest(".expense").data("person");

	var new_row = $('<tr class="row"><td><button class="expense_button delete"><i class="fa fa-times"></i></button></td><td class="item_name"><input type="text" placeholder="item" ></td><td class="cost"><input type="text" placeholder="price" ></td></tr>');


	$('#' + persons_id +' table tr:last').before(new_row);
	new_row.attr('data-owner', persons_id);
	new_row.addClass("new_row");
	$('.new_row').show("slow");

	$('.new_row').removeClass("new_row");

	// focus the cursor in the created input box
	$(this).closest('tr').prev().find('td input:first').focus();

	
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
			});
			display_update('expense ' + expense_id + ' successfully deleted');
	    }
	});

	
	//this not working either
	update_numbers();
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


// THE BELOW CODE IS NOT GETTING CALLED, ON PURPOSE
// adding row to person
// $( "#expense_area" ).on( "click", ".expense_button.add", function(){
// 	// add the row to the html first, so they can edit with no delays
// 	// alert('blolo');
// 	new_row = add_row($(this).closest('div.expense').data('person'));

// 	// then add it to the DB
// 	$.ajax({
// 	    url: '/expense/0/',
// 	    type: 'POST',
// 	    data: {
// 	    	owner: $(this).closest('.expense').data('person'),
// 	    },
// 	    success: function(result) {
// 	   	     display_update('expense ' + result + ' successfully added');
// 	   	     // ALSO, UPDATE THE above added html's id!!!
// 	    }
// 	});
// 	// ADD TO HTML
	
// });

// // ADD ROW FUNCTION
// var add_row = function(person_id){
// 	// ADD ROW IN AJAX UPON SUCCESS DO THE FOLLOWING
// 	var new_row = '<tr class="row new_row"><td><button class="expense_button delete"><i class="fa fa-times"></i></button></td><td><input type="text" placeholder="item"></td><td class="cost"><input type="text" placeholder="price"></td></tr>'
// 	$('#' + person_id +' table tr:last').before(new_row);
// 	$('.new_row').show("slow");

// 	$('.new_row').removeClass("new_row");
// 	return new_row;
// };
// END UNCALLED CODE






//******************************** Person Functions ********************************//

// Add Person
$('#add_user').click(function(){
	$('#add_user button').text('adding person...');
	$.ajax({
	    url: '/person/0/',
	    type: 'POST',
	    data: {
	    	group: $(location).attr('pathname').replace("/","").replace("/",""),
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
			display_update("person " + persons_id + " successfully created");

			// SEEMS TO COMPLICATED?
			// update the sidebar with the new person
			// Grab the last row in the totals
			// var totals_row = $('#average_row').prev().html();
			// // Insert its html before
			// $('#average_row').before(totals_row);
			// var new_row = $('#average_row').prev();
			// new_row.addClass("new_row");
			// new_row.attr("id", "sidebar_person_total_" + persons_id);
			// new_row.show("slow");
			// new_row.removeClass('new_row');


			$('#average_row').before('<tr class="sidebar_person_total new_row" id="sidebar_person_total_' + persons_id + '"><td style="color:' + persons_color +';">-----</td><td class="align_right"> 0.00 </td><td class="align_right">0.00</td></tr>');

			$('#sidebar_person_total_' + persons_id).show("slow");
			$('#sidebar_person_total_' + persons_id).removeClass('new_row');
			$('#sidebar_person_total_' + persons_id + ':first-child').css('color', '#' + persons_color);


			// // swap back the add user button text
			$('#add_user button').text('add another person');

// $('#right_info_bar').css('height', $('body').height());

	    }
	});
	update_numbers();
});


// Delete Person
$( "#expense_area" ).on( "click", ".delete_person", function(){
	
	// //double click animation, currently unused
	// $(this).text('double click to delete');
	// $(this).addClass('delete_confirmation');
	
	// // Reset if the button loses focus
	// $(this).blur(function(){
	// 	$(this).click();
	// 	$(this).text("delete person");
	// 	$(this).removeClass('delete_confirmation');
	// });
	
	var persons_name = $(this).closest(".expense").data("name");
	var persons_id = $(this).closest(".expense").data("person");

	if(typeof persons_name == "undefined"){
		persons_name = "person " + persons_id;
	}

	var delete_confirmation = confirm("delete " + persons_name + "?");
	
	if(delete_confirmation == true){
	// $(".delete_person" ).dblclick(function() { <currently unused, swap brackets below
		

		$.ajax({
		    url: '/person/' + persons_id + "/",
		    type: 'POST',
		    data: {
		    	operation: "delete",
		    },
		    success: function(result) {
   	     		//remove the person	
		   	    display_update(persons_name + ' successfully deleted');	
				// $(this).closest(".expense_wrapper").slideToggle('slow', function(){
				// 	//DO AJAX CALL THEN REMOVE
					
				// 	$(this).remove();
				// });
				
				// // Remove them from the sidebar
				// var sidebar_person = $('#sidebar_person_total_'+ $(this).closest(".expense").attr("id"));
				// sidebar_person.hide('slow', function(){
				// 	$(this).remove();
				// });
				// remove clicked element
				// msnry.remove( $('#'+result).closest('.expense'));
			  	// layout remaining item elements
				// msnry.reload();
				$('#'+result).closest('.expense').remove();
				$('#sidebar_person_total_'+ result).remove();

		    }
		});

		
	}
	// });
	
	
	// not sure why this dont work
	update_numbers();
});


// Toggle Edit Person slider
$( "#expense_area" ).on( "click", ".expense_button.edit", function(){
// $( ".expense_button.edit" ).click(function() {
	// passcode required if it exists...
	$(this).parent().next('.edit_person_wrapper').slideToggle( "fast");
	// setTimeout(msnry.reload(),500);
	// container.style.display = 'block';
	// $container.masonry();
	// $(this).closest(".expense_wrapper").toggleClass('edit_open');
	// msrny.reload();
});


// Change Person's Name
$( "#expense_area" ).on( "change", ".expense_owner input", function(){
	var owner = $(this);
	var persons_id = $(this).closest(".expense").data("person");
	var persons_old_name = $(this).closest(".expense").data("name");
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
	   	    display_update(persons_name + "\'s color successfully changed");			
	    }
	});
});


// Change Person's Email
$("#expense_area").on("change", ".email",function(){
	display_update('functionality not implemented, sorry');
});


// Change Person's Passcode
$("#expense_area").on("change", ".password",function(){
	display_update('functionality not implemented, sorry');
});
$("#expense_area").on("change", ".confirm_password",function(){
	display_update('functionality not implemented, sorry');
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

	var delete_confirmation = confirm("delete " + group_name + "?");
	
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


// No, Add/Change Group Name
// Change the value to what the group name is on click
$('#change_group_name').click(function(){
	var group_name = $(this).data('name');
	$(this).val(group_name);	
});
// switch back to the placeholder text on blur
$('#change_group_name').blur(function(){
	$(this).val("")
});
// actually do the work on change
$('#change_group_name').change(function(){
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
		   	     $("#group_name").text(result);
		   	     $("#group_name").attr("data-name", result);

		   	 }
		   	 else{
		   	 	display_update('group name changed to ' + group_id);
				$(document).attr('title', 'trek/split - ' +group_id);
				the_input_box.data("name", group_id);
				$("#group_name").text(group_id);
				$("#group_name").attr("data-name", "");	
		   	 }
	    }
	});
});

// Send Invitation Email
$('#send_email').focus(function(){
	$(this).attr("placeholder", "yolo");
});
$('#send_email').blur(function(){
	$(this).attr("placeholder", "share by email");
});
$('#send_email').click(function(){
	var email_to_invite = $('#invite_email').val();

	var group_id = $("#group_name").data("group");

	$.ajax({
	    url: '/group/' + group_id + '/',
	    type: 'POST',
	    data: {
	    	operation: 'send_invitation',
	    	email: email_to_invite,
	    },
	    success: function(result) {

	    }
	});
	display_update('functionality not implemented');
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
	else if($('#about').css('display') == 'block'){
		border_swap('#settings_button', '#about_button');
		$( "#about" ).slideToggle( "fast");
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
	//if about is open, we gotta close it
	else if ($('#about').css('display') == 'block'){
		border_swap('#share_button', '#about_button');
		$( "#about" ).slideToggle( "fast");
		$( "#share" ).slideToggle( "fast");
	}
	else{
		border_swap('#share_button', '#share_button');
		$( "#share" ).slideToggle( "fast");
	}
	// Below focuses on the email input
	$("#invite_email").focus();
});
// Toggle About Tab
$('#about_button').click(function(){
	//if settings is open, we gotta fade it out too
	if($('#settings').css('display') == 'block'){
		border_swap('#about_button', '#settings_button');
		$( "#settings" ).slideToggle( "fast");
		$( "#about" ).slideToggle( "fast");
		
	}
	//if share is open, we gotta close it
	else if($('#share').css('display') == 'block'){
		border_swap('#about_button', '#share_button');
		$( "#share" ).slideToggle( "fast");
		$( "#about" ).slideToggle( "fast");
	}
	else{
		border_swap('#about_button', '#about_button');
		$( '#about' ).slideToggle( "fast");

	}
});

// Change the Group's expense options



// Add Group Passcode
$("#right_info_bar").on("click", "#change_group_passcode",function(){
	display_update('functionality not implemented, sorry');
});



// Toggle Requirement for individual Passcodes
$("#right_info_bar").on("click", "#change_passcode_requirement",function(){
	display_update('functionality not implemented, sorry');
});

// Share Group
// $("#right_info_bar").on("click", "#send_email",function(){
// 	display_update('functionality not implemented, sorry');
// });

// Hide the advertisement... display update for now, and the buttons not even here
$("#hide_ad").click(function(){
	$('#advertisement').slideToggle("slow");
});


// includes spreadsheet export?



//******************************** General Functions ********************************//

// Update All Numbers on input change
$( "#expense_area" ).on( "change", "input", function(){
	update_numbers();
});
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

// Returns random ID, used for testing with no backend
var create_pseudo_id = function(){
	return Math.floor( (Math.random()*1000)+1);
};

// Changes the notification bar
var display_update = function( message ){
	
	$('#update_display').addClass('animated flash');
	setTimeout(function(){
		$('#update_display').text(message);
	},175);
	setTimeout(function(){
		$('#update_display').removeClass('animated flash');
	},1000);
	


};

// Updates number across the screen
var update_numbers = function(){
	// running question:
	// Do I do this in jquery? Is that more vulnerable to people fucking around?
	// it will mean less data transfer, maybe quicker UI?
	// or do I do it server side and just return everything?

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
	var average = (sum/num_expenses).toFixed(2);
	$("#total").text("$" + sum.toFixed(2));
	$("#average").text("$" + average);


	$('.expense').each(function(){
		var difference_td = $('#sidebar_person_total_' + $(this).attr('id')).children('td:nth-last-child(2)');
		var total_td = $('#sidebar_person_total_' + $(this).attr('id')).children('td:last');

		var difference = parseFloat(total_td.text())-average;

		if(difference<0){
			if(!difference_td.hasClass('negative_amount')){
				difference_td.addClass('negative_amount');
			}
		}
		else{
			if(difference_td.hasClass('negative_amount')){
				difference_td.removeClass('negative_amount');
			}			
		}

		difference_td.text(difference.toFixed(2));
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


	// UPDATES THE PAYMENT PLAN FIELDS
	// Basically, people in the red need to pay the people in the black money.

};
update_numbers();
});