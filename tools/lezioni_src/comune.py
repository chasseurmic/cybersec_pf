# -*- coding: utf-8 -*-
"""Helper condivisi per rendere le dispense veri testi di studio."""


def studio(d, sintesi=None, glossario=None, errori=None, domande=None,
           collegamenti=None, approfondimenti=None):
    """Aggiunge alla dispensa la sezione 'Per lo studio a casa'.

    - sintesi:        lista di stringhe (punti chiave da ricordare)
    - glossario:      lista di (termine, significato)
    - errori:         lista di stringhe (errori comuni da evitare)
    - domande:        lista di stringhe (domande di autoverifica)
    - collegamenti:   lista di stringhe (rimandi ad altre lezioni)
    - approfondimenti:lista di (titolo, testo) extra facoltativi
    """
    d.h1("Per lo studio a casa")

    if approfondimenti:
        for titolo, testo in approfondimenti:
            d.h2(titolo)
            d.p(testo)

    if sintesi:
        d.h2("In sintesi (i punti da ricordare)")
        d.bullets(sintesi)

    if glossario:
        d.h2("Glossario")
        d.table(["Termine", "Significato"], glossario, widths=[2600, 6426])

    if errori:
        d.h2("Errori comuni da evitare")
        d.box("rosso", "Attenzione a questi scivoloni", items=errori)

    if domande:
        d.h2("Domande di autoverifica")
        d.p("Prova a rispondere senza guardare: se ti blocchi, la risposta è nel "
            "testo della lezione. Sono ottime per ripassare prima di una verifica.")
        d.numbered(domande)

    if collegamenti:
        d.h2("Collegamenti con le altre lezioni")
        d.bullets(collegamenti)
