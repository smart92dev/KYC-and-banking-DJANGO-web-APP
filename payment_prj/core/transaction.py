from django.shortcuts import render,redirect
from core.models import Transaction
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user).order_by("-id")
    receiver_transaction = Transaction.objects.filter(receiver=request.user).order_by("-id")

    context = {
        "sender_transaction":sender_transaction,
        "receiver_transaction":receiver_transaction,
    }

    return render(request, "transaction/transaction-list.html",context)

@login_required
def transaction_detail(request,transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
            "transaction":transaction,
        }
    return render(request, "transaction/transaction-details.html",context)

