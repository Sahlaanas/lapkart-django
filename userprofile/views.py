from django.shortcuts import render, redirect
from  django.contrib.auth.decorators import login_required
from . models import User_Address
from useraccount.models import Account
from django.contrib import messages,auth
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .forms import AddressForm
from order.models import Wallet

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
    
    
@login_required(login_url='login')
def user_profile(request):
    address = User_Address.objects.filter(user=request.user)
    wallet = Wallet.objects.filter(user=request.user)
    context = {
        'address': address,
        'wallet' : wallet
    }
    return render(request,'user_account/userprofile.html', context)

def change_dp(request):
    user_id = request.user.id
    user = Account.objects.get(id=user_id)

    try:
        image = request.FILES['user_image']
        user.user_image=image
        user.save()
    except:
        pass
       
    return redirect(user_profile)

def password_edit(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = Account.objects.get(id=request.user.id)
        if not user.check_password(old_password):
            
            messages.error(request, 'Incorrect Password')
            
            return redirect(user_profile)
        else:
            if new_password == confirm_new_password:
                Pass = ValidatePassword(new_password)
                if Pass is False:
                    messages.success(request, 'Enter Strong password')
                    return redirect(user_profile)
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                messages.success(request, 'Password changed succesfully!')
                return redirect(user_profile)
            else:
                messages.success(request,'Password doesnot match.')
                return redirect(user_profile )
            
    return render(request,'user_account/userprofile.html')

def edit_profile(request):

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']

        check = [name,phone]
        for values in check:
            if values == '':
                messages.info(request,'some fields are empty')
                return redirect(user_profile)
            else:
                pass

        user_id = request.user.id
        usr = Account.objects.filter(id = user_id)
        usr.update(username = name, phone_number = phone)
    else:
        messages.info(request, 'sorry something went wrong')

    return redirect(user_profile)

def add_address(request):
    address = User_Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request,'User address added successfully')
            return redirect(user_profile)
    else:
        form = AddressForm()
    return render(request,'user_account/add_address.html',{'form':form})

def edit_address(request, address_id):
    address =User_Address.objects.get(id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(user_profile)
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'user_account/edit_address.html', {'form': form})




def delete_address(request,address_id):

    User_Address.objects.get(id=address_id).delete()

    return redirect(user_profile)

