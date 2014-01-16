from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  

from models import Group, Person, Item

colors_for_now = ['8fd0ff', 'd28fff', 'ff8fce', 'ff8f8f', 'ffd68f', 'dfff8f', '8fffa3', '8ffff0', '988fff']

# display the empty landing paged
@csrf_exempt    
def no_group(request):
	# return the empty landing page
	return render_to_response('./test.html')

# displays the main interface
@csrf_exempt    
def group(request, group_id):
	# grab all the people in the group
	people = Person.objects.filter(group_ID__exact = group_id)

	# grab all the expenses with owners in the above list
	# expenses = 

	# TIRED OF THINKING, GRABBING ALL EXPENSES FOR NOW
	expenses = Item.objects.all()

	return render_to_response('./index.html', {'people':people, 'expenses':expenses})

# handles all expense transactions
@csrf_exempt   
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


@csrf_exempt   
def person_transaction(request, person_id):
	# When the id = 0 we create a new person!
	if person_id == '0':
		# Grab the group that we're adding the person to
		group = Group.objects.get(id__exact= int(request.POST['group']))
		# Create the Person
		new_person = Person.objects.create(group_ID=group, header_color=get_me_a_color())
		# return their ID
		return HttpResponse(new_person.id)
		return render_to_response('./person.html', {'people':people, 'expenses':expenses})

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
@csrf_exempt
def group_transaction(request, group_id):
	# if groupid=0 create a new group!
	if group_id == '0':
		new_group = Group.objects.create()
		# print new_group.id
		return HttpResponse(new_group.id)


	return HttpResponse("whoa making a group transaction on group %s" % group_id)


# returns a color from a list of colors
def get_me_a_color():
	# take the first color, add it to the end of the list, then return it, creating a nice looping action
	our_color = colors_for_now.pop(0)
	colors_for_now.append(our_color)
	return our_color