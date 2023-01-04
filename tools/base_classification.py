# This is the base classification. It will get updated from the database

base_classification = {
    'house': {
        "mortgage": None,
        "repairs": None,
        'rates': None
    },
    'transport': {
        'maintenance': None,
        'parking': None,
        'tires': None,
        'registration': None,
        'fares': None
    },
    'food': {
        'groceries': None,
        'pet_food': None,
        'eating_out': {
            'nick': None,
            'bernadette': None,
            'shared': None
        },
        'alcohol': None
    },
    'utilities': {
        'electricity': None,
        'greenbin': None,
        'internet': None,
        'cellphone': {
            'bernadette': None,
            'nick': None
        }
    },
    'clothes': {
        'work': {
            'bernadette': None,
            'nick': None
        },
        'exercise': {
            'bernadette': None,
            'nick': None
        },
        'personal': {
            'bernadette': None,
            'nick': None
        }
    },
    'medical': {
        'medications': {
            'bernadette': None,
            'nick': None
        },
        'doctor': {
            'bernadette': None,
            'nick': None
        },
        'dentist': {
            'bernadette': None,
            'nick': None
        }
    },
    'insurance': {
        'health': None,
        'car' : None,
        'life': None,
        'income_protection': None,
    },
    'household': {
        'toiletries': None,
        'cleaning': None,
        'tools': None,
    },
    'personal': {
        'gym': {
            'bernadette': None,
            'nick': None
        },
        'haircut': {
            'bernadette': None,
            'nick': None
        },
        'events': {
            'bernadette': None,
            'nick': None
        },
        'education': {
            'bernadette': None,
            'nick': None
        }
    },
    'work': {
        'expense_claim': {
            'bernadette': None,
            'nick': None
        },
        'other': {
            'bernadette': None,
            'nick': None
        }
    },
    'gifts': {
        'birthday': None,
        'wedding': None,
        'christmas': None,
        'charities': None,
        'other': None
    },
    'entertainment': {
        'alcohol-bars': None,
        'movies': None,
        'subscriptions': None,
        'games': None,
        'holiday': {
            'flights': None,
            'accommodation': None,
            'food': None
        }
    },
    'transfer': {
        'between': None,
        'external_account': None
    }
}