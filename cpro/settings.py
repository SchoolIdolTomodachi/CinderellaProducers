# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from web.default_settings import DEFAULT_ENABLED_COLLECTIONS, DEFAULT_ENABLED_PAGES, DEFAULT_JAVASCRIPT_TRANSLATED_TERMS, DEFAULT_PROFILE_EXTRA_TABS
from web.utils import tourldash
from cpro import models, forms, filters, collections_settings, utils

SITE_NAME = u'Cinderella Producers'
SITE_URL = 'http://cinderella.pro/'
SITE_IMAGE = 'cpro.png'
EMAIL_IMAGE = 'cpro_banner.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.cinderella.pro/'
#SITE_STATIC_URL = '//i.cinderella.pro/'
GAME_NAME = 'IDOLM@STER Cinderella Girls Starlight Stage'
GAME_URL = 'https://itunes.apple.com/jp/app/idolmaster-cinderella-girls/id1016318735?l=en&mt=8'
GAME_DESCRIPTION = 'THE iDOLM@STER Cinderella Girls: Starlight Stage is a spin-off free-to-play rhythm game released for mobile devices.'
DISQUS_SHORTNAME = 'cinderellapro'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'

GOOGLE_ANALYTICS = 'UA-59453399-3'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'CinderellaProducers')
TWITTER_HANDLE = 'cinderella__pro'

HASHTAGS = ['imas', 'deresute', u'デレステ']

USER_COLORS = models.TYPES

GET_GLOBAL_CONTEXT = utils.globalContext

STATIC_FILES_VERSION = '15'

TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', 2) + 2
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)
FAVORITE_CHARACTER_TO_URL = lambda link: '/idol/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _(u'{nth} Favorite Idol')

LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', 2)

EMPTY_IMAGE = 'cinderella.png'

JAVASCRIPT_TRANSLATED_TERMS = DEFAULT_JAVASCRIPT_TRANSLATED_TERMS
JAVASCRIPT_TRANSLATED_TERMS += [
    'Permalink',
    'Deleted',
]

ON_USER_EDITED = utils.onUserEdited
ON_PREFERENCES_EDITED = utils.onPreferencesEdited

DONATORS_STATUS_CHOICES = models.DONATORS_STATUS_CHOICES

PROFILE_EXTRA_TABS = OrderedDict([
    ('badges', DEFAULT_PROFILE_EXTRA_TABS['badges']),
    ('favorites', {
        'icon': 'star',
        'name': _('Favorite Cards'),
        'callback': 'loadFavoriteCards',
    }),
])

ENABLED_COLLECTIONS = DEFAULT_ENABLED_COLLECTIONS

ACTIVITY_TAGS = [
    ('cards', _('New Cards')),
    ('event', _('Event')),
    ('live', _('Live')),
    ('comedy', _('Comedy')),
    ('room', _('Room Decoration')),
    ('introduction', _('Introduce yourself')),
    ('idols', _('Idols')),
    ('anime', _('Anime')),
    ('cosplay', _('Cosplay')),
    ('fanart', _('Fan made')),
    ('merch', _('Merchandise')),
    ('community', _('Community')),
    ('unrelated', _('Unrelated')),
    ('AR Idol Date', 'AR Idol Date'),
]

ENABLED_COLLECTIONS['activity']['add']['before_save'] = collections_settings.activitiesBeforeSave
ENABLED_COLLECTIONS['activity']['edit']['before_save'] = collections_settings.activitiesBeforeSave

def filterActivitiesList(queryset, parameters, request):
    if request.user.is_superuser and 'force_old' in request.GET:
        if 'owner_id' in request.GET:
            return queryset.filter(owner_id=request.GET['owner_id'])
        return queryset
    return queryset.filter(id__gt=2600)

def filterActivities(queryset, parameters, request):
    if request.user.is_superuser:
        return queryset
    return filterActivitiesList(queryset, parameters, request)

ENABLED_COLLECTIONS['activity']['edit']['filter_queryset'] = filterActivities
ENABLED_COLLECTIONS['activity']['item']['filter_queryset'] = filterActivities
ENABLED_COLLECTIONS['activity']['add']['filter_queryset'] = filterActivities
ENABLED_COLLECTIONS['activity']['list']['filter_queryset'] = filterActivitiesList

ENABLED_COLLECTIONS['badge']['add']['before_save'] = collections_settings.badgesBeforeSave
ENABLED_COLLECTIONS['badge']['edit']['before_save'] = collections_settings.badgesBeforeSave

ENABLED_COLLECTIONS['account']['list']['distinct'] = True

ENABLED_COLLECTIONS['account']['add']['form_class'] = collections_settings.getAccountForm
ENABLED_COLLECTIONS['account']['add']['back_to_list_button'] = False
ENABLED_COLLECTIONS['account']['add']['after_save'] = collections_settings.addAccountAfterSave
ENABLED_COLLECTIONS['account']['edit']['form_class'] = forms.AccountFormAdvanced

ENABLED_COLLECTIONS['account']['add']['otherbuttons_template'] = 'include/advancedButton'
ENABLED_COLLECTIONS['account']['add']['extra_context'] = collections_settings.modAccountExtraContext
ENABLED_COLLECTIONS['account']['edit']['extra_context'] = collections_settings.modAccountExtraContext
ENABLED_COLLECTIONS['account']['add']['after_template'] = 'include/accountJSstarter'
ENABLED_COLLECTIONS['account']['edit']['after_template'] = 'include/accountJSstarter'
ENABLED_COLLECTIONS['account']['add']['js_files'] = ENABLED_COLLECTIONS['account']['add'].get('js_files', []) + ['mod_account']
ENABLED_COLLECTIONS['account']['edit']['js_files'] = ENABLED_COLLECTIONS['account']['edit'].get('js_files', []) + ['mod_account']

ENABLED_COLLECTIONS['account']['add']['redirect_after_add'] = collections_settings.redirectAfterAddAccount

ENABLED_COLLECTIONS['account']['list']['before_template'] = 'include/beforeLeaderboard'
ENABLED_COLLECTIONS['account']['list']['default_ordering'] = '-level'
ENABLED_COLLECTIONS['account']['list']['filter_form'] = forms.FilterAccounts
ENABLED_COLLECTIONS['account']['list']['filter_queryset'] = filters.filterAccounts
ENABLED_COLLECTIONS['account']['list']['js_files'] = ENABLED_COLLECTIONS['account']['list'].get('js_files', []) + ['leaderboard']
ENABLED_COLLECTIONS['account']['list']['extra_context'] = collections_settings.leaderboardExtraContext
ENABLED_COLLECTIONS['account']['list']['show_add_button'] = lambda request: not request.user.is_authenticated()

ENABLED_COLLECTIONS['user']['item']['extra_context'] = collections_settings.profileGetAccountTabs
ENABLED_COLLECTIONS['user']['item']['js_files'] = ENABLED_COLLECTIONS['user']['item'].get('js_files', []) + ['profile_account_tabs', 'cards']

ENABLED_COLLECTIONS['card'] = {
    'queryset': models.Card.objects.all(),
    'title': _('Card'),
    'plural_title': _('Cards'),
    'icon': 'cards',
    'list': {
        'default_ordering': '-release_date',
        'full_width': True,
        'ajax_pagination_callback': 'updateCards',
        'js_files': ['cards'],
        'filter_form': forms.FilterCards,
        'filter_queryset': filters.filterCards,
        'before_template': 'include/beforeCards',
        'after_template': 'include/afterCards',
        'extra_context': collections_settings.cardsExtraContext,
    },
    'item': {
        'ajax_callback': 'updateCardsAndOwnedCards',
        'js_files': ['cards', 'collection'],
        'filter_queryset': filters.filterCard,
        'extra_context': collections_settings.cardExtraContext,
    },
    'add': {
        'form_class': forms.CardForm,
        'multipart': True,
        'staff_required': True,
    },
    'edit': {
        'form_class': forms.CardForm,
        'multipart': True,
        'staff_required': True,
    },
}

ENABLED_COLLECTIONS['ownedcard'] = {
    'queryset': models.OwnedCard.objects.all().select_related('card'),
    'title': _('Card'),
    'plural_title': _('Cards'),
    'icon': 'album',
    'navbar_link': False,
    'list': {
        'default_ordering': '-card__i_rarity,-awakened,-card__release_date,card__idol__i_type',
        'per_line': 6,
        'page_size': 48,
        'filter_queryset': filters.filterOwnedCards,
        'col_break': 'xs',
        'foreach_items': collections_settings.foreachOwnedCard,
        'filter_form': forms.FilterOwnedCards,
        'js_files': ['ownedcards'],
        'ajax_pagination_callback': 'updateOwnedCards',
        'before_template': 'include/beforeOwnedCards',
    },
    'edit': {
        'form_class': forms.EditOwnedCardForm,
        'filter_queryset': lambda q, p, r: q.select_related('account'), # Used when checking if the center has been updated
        'redirect_after_edit': collections_settings.ownedCardRedirectAfter,
        'redirect_after_delete': collections_settings.ownedCardRedirectAfter,
        'allow_delete': True,
        'back_to_list_button': False,
        'js_files': ['edit_ownedcard'],
    },
    'item': {
        'comments_enabled': False,
        'js_files': ['ownedcards'],
    },
}

ENABLED_COLLECTIONS['idol'] = {
    'queryset': models.Idol.objects.all(),
    'title': _('Idol'),
    'plural_title': _('Idols'),
    'icon': 'idolized',
    'list': {
        'default_ordering': '-_cache_total_fans',
        'per_line': 4,
        'ajax_pagination_callback': 'ajaxModals',
        'filter_form': forms.FilterIdols,
        'filter_queryset': filters.filterIdols,
        'extra_context': collections_settings.idolsExtraContext,
        'js_files': ['idols'],
    },
    'item': {
        'template': 'idolInfo',
        'js_files': ['idolInfo'],
    },
    'add': {
        'form_class': forms.IdolForm,
        'multipart': True,
        'staff_required': True,
    },
    'edit': {
        'form_class': forms.IdolForm,
        'multipart': True,
        'staff_required': True,
    },
}

ENABLED_COLLECTIONS['event'] = {
    'queryset': models.Event.objects.all(),
    'title': _('Event'),
    'plural_title': _('Events'),
    'icon': 'event',
    'list': {
        'default_ordering': '-end',
        'per_line': 1,
        'filter_form': forms.FilterEvents,
        'filter_queryset': filters.filterEvents,
        'extra_context': collections_settings.eventsExtraContext,
        'before_template': 'include/beforeEvents',
    },
    'item': {
        'template': 'eventInfo',
        'js_files': ['bower/countdown/dest/jquery.countdown.min', 'event'],
    },
    'add': {
        'form_class': forms.EventForm,
        'multipart': True,
        'staff_required': True,
    },
    'edit': {
        'form_class': forms.EventForm,
        'multipart': True,
        'staff_required': True,
    },
}

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['index']['custom'] = True

ENABLED_PAGES['cardstat'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['cardcollection'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['addcard'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['favoritecard'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['account_about'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('account', '\d+'),
    ],
}
