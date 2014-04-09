from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie 
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required # <<<< added for authenticaton 
from django.contrib.auth import authenticate, login

from models import Group, Person, Item

colors_for_now = ['e5a7ab', 'ecc8bc', 'ffe1c7', 'fcedca', 'e8e1b0', 'c6d5b5', 'c2e5ee', 'dce0ef', 'ead8ff', 'e2bad4']

# display the empty landing paged
@ensure_csrf_cookie   
def no_group(request):
	# return the empty landing page
	return render_to_response('./test.html')

def passcode(request):
	return render_to_response('./passcode.html')

# displays the main interface
# @login_required
@ensure_csrf_cookie    
def group(request, group_id):
	# Or the alternate, redirect to create group page
	try:
		group = Group.objects.get(pk=group_id)
	except Group.DoesNotExist:
		return redirect('/')

	if request.user.is_authenticated() or group.passcode == None:
		# If the group does not exist return 404
		# group = get_object_or_404(Group, pk=group_id)


		# grab all the people in the group
		people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

		# grab all the expenses with owners in the above list
		# expenses = 

		# TIRED OF THINKING, GRABBING ALL EXPENSES FOR NOW
		# expenses = Person.item_set
		expenses = Item.objects.all().order_by('id')

		return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})
	else:
		return render_to_response('./passcode.html', {'group':group})

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
		# delete their expenses
		Item.objects.filter(person_ID = person_id).delete()
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
		current_group = Group.objects.get(id__exact=group_id)
		email_to_invite = request.POST['email']
		if current_group.name is None:
			subject = 'Help split up expenses for group ' + group_id
		else:	
			subject = 'Help split up expenses for ' + current_group.name
		body = 'Join your friends here - http://www.treksplit.com/' + group_id + '/'
		sender = 'treksplit@gmail.com'
		send_mail(subject, body, sender, [email_to_invite], fail_silently=False)
		return HttpResponse('email sent to ' + email_to_invite)

	elif request.POST['operation'] == "change_passcode":
		current_group = Group.objects.get(id__exact=group_id)
		current_group.passcode = request.POST['passcode']
		current_group.save()
		return HttpResponse('passcode changed')

	elif request.POST['operation'] == "delete":
		current_group = Group.objects.get(id__exact=group_id)
		current_people = Person.objects.filter(group_ID__exact = group_id)
		# Grab all the relevant expenses... so we can throw them in the fire
		current_people.delete()
		current_group.delete()
		return HttpResponse(group_id)
	elif request.POST['operation'] == "authenticate":
		passcode = request.POST['passcode']
		group = authenticate(username = group_id, password = passcode)
		print group
		if group is not None:
			login(request,group)
			return HttpResponse(group_id)
		else:
			return HttpResponse(group_id)


	return HttpResponse("whoa making a group transaction on group %s" % group_id)


# returns a color from a list of colors
def get_me_a_color():
	# take the first color, add it to the end of the list, then return it, creating a nice looping action
	our_color = colors_for_now.pop(0)
	colors_for_now.append(our_color)
	return our_color