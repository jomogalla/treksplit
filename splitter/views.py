import datetime
import string, random

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie 
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required # <<<< added for authenticaton 
from django.contrib.auth import authenticate, login


from models import Group, Person, Item

colors_for_now = ['e5a7ab', 'ecc8bc', 'ffe1c7', 'fcedca', 'e8e1b0', 'c6d5b5', 'c2e5ee', 'dce0ef', 'ead8ff', 'e2bad4']

# display the empty landing paged
@ensure_csrf_cookie   
def no_group(request):
	# return the empty landing page
	return render_to_response('./welcome.html')

@ensure_csrf_cookie 
def passcode(request):
	return render_to_response('./passcode.html')

# displays the main interface
# @login_required
@ensure_csrf_cookie    
def group(request, group_id="1"):
	# if the requested group does not exist redirect to create group page
	try:
		group = Group.objects.get(pk=group_id)
	except Group.DoesNotExist:
		return redirect('/')

	# redirect groups with ids less than 250
	# dont know if people still need them
	# otherwise no go 
	if int(group_id) < int(250):
		return redirect('/' + str(group.url_hash) + '/')
	# else if int(group_id) == 1:
	# 	group = get_object_or_404(Group, pk=group_id)

	# 	# grab all the people in the group
	# 	people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

	# 	# grab all the expenses with owners in the above list
	# 	# expenses = 

	# 	# TIRED OF THINKING, GRABBING ALL EXPENSES FOR NOW
	# 	# expenses = Person.item_set
	# 	expenses = Item.objects.all().order_by('id')

	# 	return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})
	else:
		return redirect('/')

	# insecure_passcode = ""
	# if request.method == 'POST':
	# 	insecure_passcode = request.POST['passcode']

	# if group.passcode == insecure_passcode or group.passcode == None:
	# 	# If the group does not exist return 404
	# 	# group = get_object_or_404(Group, pk=group_id)

	# 	# grab all the people in the group
	# 	people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

	# 	# grab all the expenses with owners in the above list
	# 	# expenses = 

	# 	# TIRED OF THINKING, GRABBING ALL EXPENSES FOR NOW
	# 	# expenses = Person.item_set
	# 	expenses = Item.objects.all().order_by('id')

	# 	return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})
	# else:
	# 	return render_to_response('./passcode.html', {'group':group}, context_instance=RequestContext(request))

# Example creates a new group that is pre-populated
@ensure_csrf_cookie 
def example(request, group_hash):
	# Grab the group's ID
	group_id = group.id

	# If the group does not exist return 404
	# group = get_object_or_404(Group, pk=group_id)

	# grab all the people in the group
	people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

	# grab all the expenses with owners in the above list
	# expenses = 

	# Grab expenses owned by the people in the group
	expenses = []
	for person in people:
		expenses_temp = list(Item.objects.filter(person_ID__exact = person.id).order_by('id'))
		expenses = expenses + expenses_temp

	return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})


@ensure_csrf_cookie 
def group_hash(request, group_hash):
	# Or the alternate, redirect to create group page
	try:
		group = Group.objects.get(url_hash=group_hash)
	except Group.DoesNotExist:
		return redirect('/')
	
	# Grab the passcode if the request was a POST
	insecure_passcode = ""
	if request.method == 'POST':
		insecure_passcode = request.POST['passcode']

	# Grab the group's ID
	group_id = group.id

	# If the submitted passcode is the same as the groups or
	# If the group has no passcode
	# proceed
	if group.passcode == insecure_passcode or group.passcode == None or group.passcode == "":
		# If the group does not exist return 404
		# group = get_object_or_404(Group, pk=group_id)

		# grab all the people in the group
		people = Person.objects.filter(group_ID__exact = group_id).order_by('id')

		# grab all the expenses with owners in the above list
		# expenses = 

		# Grab expenses owned by the people in the group
		expenses = []
		for person in people:
			expenses_temp = list(Item.objects.filter(person_ID__exact = person.id).order_by('id'))
			expenses = expenses + expenses_temp

		return render_to_response('./index.html', {'people':people, 'expenses':expenses, 'group':group})
	# otherwise send them to the passcode page
	else:
		return render_to_response('./passcode.html', {'group':group}, context_instance=RequestContext(request))

# handles all expense transactions
def expense_transaction(request, expense_id):
	# if there are no expenses
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
		if request.POST['price'] == "":
			current_expense.price = None
		else:
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

	# Changing a Person's Color
	elif request.POST['operation'] == 'change_color':
		stripped_color = request.POST['color'][1:]
		current_person = Person.objects.get(id__exact=person_id)
		current_person.header_color = stripped_color
		current_person.save()
		return HttpResponse(person_id)

	# Changing a Person's Email
	elif request.POST['operation'] == 'change_email':

		email = request.POST['email']

		current_person = Person.objects.get(id__exact=person_id)
		current_group = current_person.group_ID
		current_person.email = email
		current_person.save()

		# using the group's name if there is one
		if current_group.name is None:
			body = 'Your email ( ' + email + ')  has been added to a Trek/Split group.\n \n Here is the link - http://www.treksplit.com/' + str(current_group.url_hash) + '/'
			subject = 'You have been added to a Trek/Split group'
		else:
			body = 'Your email ( ' + email + ')  has been added to the Trek/Split group - ' + current_group.name + '.\n \n Here is the link - http://www.treksplit.com/' + str(current_group.url_hash) + '/'
			subject = 'You have been added to a Trek/Split group - ' + current_group.name

		# body = 'Your email ( %s )  has been added to the Trek/Split group %s.\n \n Here is the link - http://www.treksplit.com/%s/' % (email,group_title,current_group.id)
		sender = 'treksplit@gmail.com'
		send_mail(subject, body, sender, [email], fail_silently=False)

		return HttpResponse(person_id)


	#finalizing a person's expenses
	elif request.POST['operation'] == 'finalize':
		current_person = Person.objects.get(id__exact=person_id)
		current_person.finalized = True
		current_person.save()
		current_group = current_person.group_ID
		# check if everyone in the group is finalized, then send an email
		group_members = Person.objects.filter(group_ID__exact = current_group.id)

		whole_group_finalized = True
		for person in group_members:
			if not person.finalized:
				whole_group_finalized = False

		# Everyone is finalized - send an email out
		if whole_group_finalized:
			if current_group.name is None:
				group_title = str(current_group.url_hash)
			else:
				group_title = current_group.name

			# grab everyone's emails
			member_emails = []
			for person in group_members:
				if person.email is not None:
					member_emails.append(person.email)

			if member_emails is not None:
				body = 'Everyone has finished inputting their expenses. \n \n Follow the link to find out who you owe (or who owes you). \n http://www.treksplit.com/' + str(current_group.id) + '/'
				subject = 'Trek/Split - ' + group_title + ' - Finished!'
				sender = 'treksplit@gmail.com'
				send_mail(subject, body, sender, member_emails, fail_silently=False)


		return HttpResponse(person_id)
		
	#unfinalizing a person's expenses
	elif request.POST['operation'] == 'unfinalize':
		current_person = Person.objects.get(id__exact=person_id)
		current_person.finalized = False
		current_person.save()
		return HttpResponse(person_id)
		
	return HttpResponse("changin peoples huh, specifically # %s" % person_id)


# Handles all group transactions
def group_transaction(request, group_id):
	# if groupid=0 create a new group!
	if group_id == '0':
		new_group = Group.objects.create()
		# print new_group.id
		new_group.url_hash = gen_hash(new_group.id)
		new_group.save()
		return HttpResponse(new_group.url_hash)

	# Change Group Name
	elif request.POST['operation'] == "change_name":
		current_group = Group.objects.get(id__exact=group_id)
		current_group.name = request.POST['name']
		current_group.save()
		return HttpResponse(current_group.name)

	# Send Email Invite for Group
	elif request.POST['operation'] == "send_invitation":
		current_group = Group.objects.get(id__exact=group_id)
		email_to_invite = request.POST['email']
		if current_group.name is None:
			subject = 'Help split up expenses'
		else:	
			subject = 'Help split up expenses for ' + current_group.name
		body = 'Join your friends here - http://www.treksplit.com/' + current_group.url_hash + '/'
		sender = 'treksplit@gmail.com'
		send_mail(subject, body, sender, [email_to_invite], fail_silently=False)
		return HttpResponse('email sent to ' + email_to_invite)

	# Change passcode
	elif request.POST['operation'] == "change_passcode":
		current_group = Group.objects.get(id__exact=group_id)
		current_group.passcode = request.POST['passcode']
		current_group.save()
		if current_group.passcode == "":
			return HttpResponse('passcode removed')
		else:
			return HttpResponse('passcode changed')

	# Delete Group
	elif request.POST['operation'] == "delete":
		current_group = Group.objects.get(id__exact=group_id)
		current_people = Person.objects.filter(group_ID__exact = group_id)
		# Grab all the relevant expenses... so we can throw them in the fire
		current_people.delete()
		current_group.delete()
		return HttpResponse(group_id)

	# Authenticate - CURRENTLY UNUSED
	elif request.POST['operation'] == "authenticate":
		passcode = request.POST['passcode']
		group = authenticate(username = group_id, password = passcode)
		if group is not None:
			login(request,group)
			return HttpResponse(group_id)
		else:
			return HttpResponse(group_id)
	# Change Group Deadline
	elif request.POST['operation'] == "change_deadline":
		new_deadline = request.POST['deadline']
		print new_deadline
		current_group = Group.objects.get(id__exact=group_id)
		current_group.deadline = new_deadline
		current_group.save()
		return HttpResponse(group_id)

	# Default Catch-All that does nothing
	return HttpResponse("whoa making a group transaction on group %s" % group_id)

# Generates the url for groups, using the group id as seed
def gen_hash(seed):
    base = string.ascii_letters+string.digits # Output hash base: all alphabets and digits
    random.seed(seed) # Input string as the random seed
    hash_value = ""
    for i in range(6):
        # Generate a 10-character hash by randomly select characters from base
        hash_value += random.choice(base)
    return hash_value

# returns a color from a list of colors
def get_me_a_color():
	# take the first color, add it to the end of the list, then return it, creating a nice looping action
	our_color = colors_for_now.pop(0)
	colors_for_now.append(our_color)
	return our_color