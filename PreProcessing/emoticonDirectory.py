def select_emoticon(x):
    return {
        ":)"  : 'happy',
        ":("  : 'sad',
        ":o"  : 'surprised',
        ":-*" : 'kizz',
        ":-D" : 'laugh',
        ">:-o": 'angry',
        "=D>" : 'applause',
        ">:D<": 'hug',
        ":-\\": 'undecided',
        ":-|" : 'whatever',
        ";-)" : 'wink',
        "8-)" : 'cool',
        ":'(" : 'cry',
        "<:-|": 'foolish',
        ":-!" : 'foot in mouth',
        "X;{" : 'sick',
        ":D" : 'big grin'

    }.get(x, x)