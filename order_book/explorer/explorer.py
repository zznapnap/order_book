from book.models import Order, Trade, HistoryTrade, Token
from django.core import serializers
from django.db.models import Q
from django.forms.models import model_to_dict
import json

def get_user_order_list(page_size, user_id):
    order_list = list(Order.objects.filter(user_id=user_id).values('type', 'token_id', 'price', 'amount', 'timestamp').order_by('-timestamp')[:page_size])
    order_list = {'order':order_list}
    order_list = json.dumps(order_list)
    order_list = json.loads(order_list)
    return order_list

def get_user_trade_list(page_size, user_id):
    trade_list = list(Trade.objects.filter(Q(seller=user_id) | Q(buyer=user_id)).order_by('-timestamp')[:page_size])
    trade_list_with_type = []
    for i in trade_list:

        if i.buyer == user_id:
            buy_dict = {}
            buy_dict['price'] = i.__dict__['price']
            buy_dict['amount'] = i.__dict__['amount']
            buy_dict['timestamp'] = i.__dict__['timestamp']
            buy_dict['token_id'] = i.__dict__['token_id']
            buy_dict['type'] = 0
            trade_list_with_type.append(buy_dict)

        if i.seller == user_id:
            sell_dict = {}
            sell_dict['price'] = i.__dict__['price']
            sell_dict['amount'] = i.__dict__['amount']
            sell_dict['timestamp'] = i.__dict__['timestamp']
            sell_dict['token_id'] = i.__dict__['token_id']
            sell_dict['type'] = 1
            trade_list_with_type.append(sell_dict)

    trade_list = {'order':trade_list_with_type}
    trade_list = json.dumps(trade_list)
    trade_list = json.loads(trade_list)
    return trade_list

def get_order_book(page_size, token_id):
    order_list = []
    order_list.append(list(Order.objects.filter(type=0, token_id=token_id).values('price', 'amount').order_by('-price')[:page_size]))
    order_list.append(list(Order.objects.filter(type=1, token_id=token_id).values('price', 'amount').order_by('price')[:page_size]))
    for i in range(0,2):
        order_list[i] = json.dumps(order_list[i])
        order_list[i] = json.loads(order_list[i])
    return order_list

def get_trade_record(since, until, token_id):
    trade_record = serializers.serialize('json', HistoryTrade.objects.filter(token_id=token_id, timestamp__gte=since, timestamp__lte=until).order_by('timestamp'))
    trade_record = json.loads(trade_record)
    return trade_record