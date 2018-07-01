import json
import codecs
import pdfkit
import sys
import cgi
from urllib import request

reader = codecs.getreader('utf-8')
IMAGE_URL_BASE = 'http://netrunnerdb.com/card_image/{code}.png'
DECK_URL_BASE = 'http://www.netrunnerdb.com/api/2.0/public/deck/'

ALL_CARDS_URL = 'http://netrunnerdb.com/api/2.0/public/cards'

# card_sheet = ''
card_base = '<div class="card"><img class="card-img" src="{url}" /></div>\n'
# output = ''


def get_identities():
    cards_str = request.urlopen(ALL_CARDS_URL)
    cards = json.load(reader(cards_str))
    identities = []
    for card in cards["data"]:
        if card["type_code"] == "identity":
            identities.append(card["code"])
    return identities


def add_to_card_sheet(card_sheet, cards):
    for card in cards:
        x = cards[card]
        # if x > 3:
        #     x = 1
        while x > 0:
            card_sheet += card_base.format(
                url=IMAGE_URL_BASE.format(code=card)
            )
            x -= 1
    return card_sheet


def print_page(card_sheet):
    output = '''<html>
              <style>
               .card{
                 float: left;
               }
               .card-img{
               width:2.5in;
              }
              </style>
              <body>'''
    output += card_sheet
    output += '</body></html>'
    return output


def runner(arguments, identity):
    card_sheet = ''
    identities = get_identities()

    for deck in arguments:
        decklist_str = request.urlopen(DECK_URL_BASE + str(deck))
        decklist = json.load(reader(decklist_str))

        cards = decklist['data'][0]['cards']

        card_codes = list(cards)

        for card in card_codes:
            if card in identities:
                if identity:
                    card_sheet = add_to_card_sheet(card_sheet, {card: 1})
                cards.pop(card)

        card_sheet = add_to_card_sheet(card_sheet, cards)

    return print_page(card_sheet)
    # html_file = open('output.html', 'w')
    #
    # html_file.write(output)
    # html_file.close()
    # pdfkit.from_url('output.html', 'output.pdf')



if __name__ == '__main__':
    form = cgi.FieldStorage()

    identity = form.getvalue('identity')
    decks = form.getvalue('decks').split(',')

    runner(identity, decks)

    # if len(sys.argv) == 1 or (
    #         '-identity' in sys.argv
    #         and len(sys.argv) == 1):
    #     print("Please add at least one NRDB deck ID (from your own shared decklist page).")
    # else:
    #     if '-identity' in sys.argv:
    #         identity = sys.argv.indexOf('-identity')
    #         arguments = sys.argv[1:identity] + sys.argv[identity + 1:]
    #     else:
    #         arguments = sys.argv[1:]
    #         identity = 0
    #     print("Running for these decklists: ", arguments)
    #     runner(arguments, identity > -1)
