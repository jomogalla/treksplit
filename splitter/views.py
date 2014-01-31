from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie 
from django.core.context_processors import csrf
from django.core.mail import send_mail

from models import Group, Person, Item

colors_for_now = ['e5a7ab', 'ecc8bc', 'ffe1c7', 'fcedca', 'e8e1b0', 'c6d5b5', 'c2e5ee', 'dce0ef', 'ead8ff', 'e2bad4']

# display the empty landing paged
@ensure_csrf_cookie   
def no_group(request):
	# return the empty landing page
	return render_to_response('./test.html')

# displays the main interface
@ensure_csrf_cookie    
def group(request, group_id):
	# grab all the people in the group
	people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

	# If the group does not exist return 404
	# group = get_object_or_404(Group, pk=group_id)

	# Or the alternate, redirect to create group page
	try:
		group = Group.objects.get(pk=group_id)
	except Group.DoesNotExist:
		return redirect('/')


	# grab all the expenses with owners in the above list
	# expenses = 

	# TIRED OF THINKING, GRABBING ALL EXPENSES FOR NOW
	expenses = Item.objects.all().order_by('id')

	return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})


# handles all expense transactions
def expense_transaction(request, expense_id):
	# if there are no expensez
	if expense_id == '0':
		# Grabbing the owner of the expense
		owner = Person.objects.get(id__exact= int(request.POST['owner']))

		# creating expense
		new_expense = Item.objects.create(person_ID=owner)
		return HttpResponse(new_expense.id)
	
	# delete the expense
	elif request.POST['operation'] == 'delete':
		Item.objects.get(id__exact=expense_id).delete()
		return HttpResponse(expense_id)

	# Changing an expense's name
	elif request.POST['operation'] == 'change_name':
		current_expense = Item.objects.get(id__exact=expense_id)
		current_expense.name = request.POST['name']
		current_expense.save()
		return HttpResponse(expense_id)

	# Changing an expense's price
	elif request.POST['operation'] == 'change_price':
		current_expense = Item.objects.get(id__exact=expense_id)
		current_expense.price = request.POST['price']
		current_expense.save()
		return HttpResponse(expense_id)
	else:
		return HttpResponse("uhhh something went wrong")


 # handles all person transactions
def person_transaction(request, person_id):
	# When the id = 0 we create a new person!
	if person_id == '0':
		# Grab the group that we're adding the person to
		group = Group.objects.get(id__exact= int(request.POST['group']))
		# Create the Person
		new_person = Person.objects.create(group_ID=group, header_color=get_me_a_color())
		# return their ID
		# return HttpResponse(new_person.id)
		return render_to_response('./person.html', {'person':new_person,})

	# Deleting a Person
	elif request.POST['operation'] == 'delete':
		# delete all the expenses(items)
		# ^^^ to be implemented ^^^
		# delete the person
		Person.objects.get(id__exact=person_id).delete()
		return HttpResponse(person_id)

	# Changing a Person's name
	elif request.POST['operation'] == 'change_name':
		current_person = Person.objects.get(id__exact=person_id)
		current_person.name = request.POST['name']
		current_person.save()
		return HttpResponse(person_id)

	# Changing a Person's
	elif request.POST['operation'] == 'change_color':
		stripped_color = request.POST['color'][1:]
		current_person = Person.objects.get(id__exact=person_id)
		current_person.header_color = stripped_color
		current_person.save()
		return HttpResponse(person_id)

	return HttpResponse("changin peoples huh, specifically # %s" % person_id)


# Handles all group transactions
def group_transaction(request, group_id):
	# if groupid=0 create a new group!
	if group_id == '0':
		new_group = Group.objects.create()
		# print new_group.id
		return HttpResponse(new_group.id)

	elif request.POST['operation'] == "change_name":
		current_group = Group.objects.get(id__exact=group_id)
		current_group.name = request.POST['name']
		current_group.save()
		return HttpResponse(current_group.name)

	elif request.POST['operation'] == "send_invitation":
		print "1"
		current_group = Group.objects.get(id__exact=group_id)
		print current_group
		email_to_invite = request.POST['email']
		print email_to_invite
		subject = 'Join us in splitting up the expenses for ' + current_group.name
		print subject
		body = 'Here is the url:<br>http://www.treksplit.com/' + group_id + '/'
		print body
		sender = 'jason@treksplit.com'
		print sender
		send_mail(subject, body, sender, email_to_invite, fail_silently=False)
		print "7"
		return HttpResponse('email sent')



	return HttpResponse("whoa making a group transaction on group %s" % group_id)


# returns a color from a list of colors
def get_me_a_color():
	# take the first color, add it to the end of the list, then return it, creating a nice looping action
	our_color = colors_for_now.pop(0)
	colors_for_now.append(our_color)
	return our_color