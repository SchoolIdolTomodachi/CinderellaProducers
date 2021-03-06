from django.db.models import Q
from django.core.exceptions import PermissionDenied
from cpro import models

############################################################
# Cards

def filterCards(queryset, parameters, request):
    if request.user.is_authenticated():
        request.user.all_accounts = request.user.accounts.all()
        accounts_pks = ','.join([str(account.pk) for account in request.user.all_accounts])
        if accounts_pks:
            queryset = queryset.extra(select={
                'total_owned': 'SELECT COUNT(*) FROM cpro_ownedcard WHERE card_id = cpro_card.id AND account_id IN ({})'.format(accounts_pks),
                'favorited': 'SELECT COUNT(*) FROM cpro_favoritecard WHERE card_id = cpro_card.id AND owner_id IN ({})'.format(request.user.id),
            })
    if 'favorite_of' in parameters and parameters['favorite_of']:
        queryset = queryset.filter(fans__owner_id=parameters['favorite_of'])
    if 'ids' in parameters and parameters['ids']:
        queryset = queryset.filter(id__in=parameters['ids'].split(','))
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(idol__name__icontains=term)
                                       | Q(idol__japanese_name__icontains=term)
                                       | Q(title__icontains=term)
                                       | Q(translated_title__icontains=term)
                                       | Q(skill_name__icontains=term)
                                       | Q(translated_skill_name__icontains=term)
                                   )
    if 'i_rarity' in parameters and parameters['i_rarity']:
        queryset = queryset.filter(i_rarity=parameters['i_rarity'])
    if 'type' in parameters and parameters['type']:
        queryset = queryset.filter(idol__i_type=parameters['type'])
    if 'is_event' in parameters and parameters['is_event']:
        if parameters['is_event'] == '2':
            queryset = queryset.filter(event__isnull=False)
        elif parameters['is_event'] == '3':
            queryset = queryset.filter(event__isnull=True)
    if 'is_limited' in parameters and parameters['is_limited']:
        if parameters['is_limited'] == '2':
            queryset = queryset.filter(is_limited=True)
        elif parameters['is_limited'] == '3':
            queryset = queryset.filter(is_limited=False)
    if 'has_art' in parameters and parameters['has_art']:
        if parameters['has_art'] == '2':
            queryset = queryset.filter(art__isnull=False).exclude(art='')
        elif parameters['has_art'] == '3':
            queryset = queryset.filter(Q(art__isnull=True) | Q(art=''))
    if 'has_art_hd' in parameters and parameters['has_art_hd']:
        if parameters['has_art_hd'] == '2':
            queryset = queryset.filter(art_hd__isnull=False).exclude(art_hd='')
        elif parameters['has_art_hd'] == '3':
            queryset = queryset.filter(Q(art_hd__isnull=True) | Q(art_hd=''))
    if 'i_skill' in parameters and parameters['i_skill']:
        queryset = queryset.filter(i_skill=parameters['i_skill'])
    if 'leader_skill' in parameters and parameters['leader_skill']:
        value = parameters['leader_skill']
        if value.startswith('type-'):
            queryset = queryset.filter(leader_skill_type=int(value[5:]))
        elif value.startswith('apply-'):
            queryset = queryset.filter(leader_skill_apply=int(value[6:]))
    if 'idol' in parameters and parameters['idol']:
        queryset = queryset.filter(idol=parameters['idol'])
    if 'event' in parameters and parameters['event']:
        queryset = queryset.filter(event=parameters['event'])
    return queryset

def filterCard(queryset, parameters, request):
    queryset = filterCards(queryset, parameters, request)
    return queryset

############################################################
# Idols

def filterIdols(queryset, parameters, request):
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(name__icontains=term)
                                       | Q(japanese_name__icontains=term)
                                       | Q(romaji_hometown__icontains=term)
                                       | Q(hometown__icontains=term)
                                       | Q(hobbies__icontains=term)
                                       | Q(CV__icontains=term)
                                       | Q(romaji_CV__icontains=term)
                                   )
    if 'type' in parameters and parameters['type']:
        queryset = queryset.filter(i_type=parameters['type'])
    if 'i_blood_type' in parameters and parameters['i_blood_type']:
        queryset = queryset.filter(i_blood_type=parameters['i_blood_type'])
    if 'i_writing_hand' in parameters and parameters['i_writing_hand']:
        queryset = queryset.filter(i_writing_hand=parameters['i_writing_hand'])
    if 'i_astrological_sign' in parameters and parameters['i_astrological_sign']:
        queryset = queryset.filter(i_astrological_sign=parameters['i_astrological_sign'])
    if 'has_signature' in parameters and parameters['has_signature']:
        if parameters['has_signature'] == '2':
            queryset = queryset.filter(signature__isnull=False).exclude(signature='')
        elif parameters['has_signature'] == '3':
            queryset = queryset.filter(Q(signature__isnull=True) | Q(signature=''))
    return queryset

############################################################
# Accounts

def filterAccounts(queryset, parameters, request):
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(owner__username__icontains=term)
                                       | Q(owner__email__iexact=term)
                                       | Q(nickname__icontains=term)
                                       | Q(device__icontains=term)
                                       | Q(owner__preferences__description__icontains=term)
                                       | Q(owner__preferences__location__icontains=term)
                                   )
    if 'own_card' in parameters and parameters['own_card']:
        queryset = queryset.filter(ownedcards__card__id=parameters['own_card'])
    if 'favorite_card' in parameters and parameters['favorite_card']:
        queryset = queryset.filter(owner__favoritecards__card__id=parameters['favorite_card'])
    if 'user_type' in parameters and parameters['user_type']:
        queryset = queryset.filter(owner__preferences__color=unicode(parameters['user_type']))
    if 'game_id' in parameters and parameters['game_id']:
        queryset = queryset.filter(game_id=parameters['game_id'])
    if 'favorite_character' in parameters and parameters['favorite_character']:
        queryset = queryset.filter(Q(owner__preferences__favorite_character1=parameters['favorite_character'])
                                 | Q(owner__preferences__favorite_character2=parameters['favorite_character'])
                                 | Q(owner__preferences__favorite_character3=parameters['favorite_character'])
                               )
    if 'starter_id' in parameters and parameters['starter_id']:
        queryset = queryset.filter(starter_id=parameters['starter_id'])
    if 'center_type' in parameters and parameters['center_type']:
        queryset = queryset.filter(center__card__idol__i_type=parameters['center_type'])
    if 'center_rarity' in parameters and parameters['center_rarity']:
        queryset = queryset.filter(center__card__i_rarity=parameters['center_rarity'])
    if 'accept_friend_requests' in parameters and parameters['accept_friend_requests']:
        if parameters['accept_friend_requests'] == '2':
            queryset = queryset.filter(accept_friend_requests=True)
        elif parameters['accept_friend_requests'] == '3':
            queryset = queryset.filter(accept_friend_requests=False)
    if 'ordering' in parameters:
        if parameters['ordering'] == 'level':
            queryset = queryset.exclude(level=0).exclude(level=None)
        if parameters['ordering'] == 'start_date':
            queryset = queryset.exclude(start_date=None)
    return queryset

############################################################
# Events

def filterEvents(queryset, parameters, request):
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(name__icontains=term)
                                       | Q(translated_name__icontains=term)
            )
    if 'i_kind' in parameters and parameters['i_kind']:
        queryset = queryset.filter(i_kind=parameters['i_kind'])
    if 'idol' in parameters and parameters['idol']:
        queryset = queryset.filter(cards__idol=parameters['idol'])
    return queryset

############################################################
# Owned Cards

def filterFavoriteCards(queryset, parameters, request):
    if 'owner' in parameters:
        queryset = queryset.filter(owner_id=parameters['owner'])
    else:
        raise PermissionDenied()
    return queryset

############################################################
# Owned Cards

def filterOwnedCards(queryset, parameters, request):
    if 'account' in parameters:
        queryset = queryset.filter(account_id=parameters['account'])
    elif 'ids' in parameters and parameters['ids']:
        queryset = queryset.filter(id__in=parameters['ids'].split(','))
    else:
        raise PermissionDenied()
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(card__title__icontains=term)
                                       | Q(card__idol__name__icontains=term)
                                   )
    if 'i_rarity' in parameters and parameters['i_rarity']:
        queryset = queryset.filter(card__i_rarity=parameters['i_rarity'])
    if 'is_event' in parameters and parameters['is_event']:
        if parameters['is_event'] == '2':
            queryset = queryset.filter(card__event__isnull=False)
        elif parameters['is_event'] == '3':
            queryset = queryset.filter(card__event__isnull=True)
    if 'type' in parameters and parameters['type']:
        queryset = queryset.filter(card__idol__i_type=parameters['type'])
    if 'i_skill' in parameters and parameters['i_skill']:
        queryset = queryset.filter(card__i_skill=parameters['i_skill'])
    return queryset
