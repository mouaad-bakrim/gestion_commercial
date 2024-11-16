from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
import math
from reportlab.lib.styles import getSampleStyleSheet
from .pdf_utils_fact import draw_page_nb, draw_footer,draw_info, draw_document_info, draw_orderly_simple_table, draw_header, \
    draw_summary_table, background_text


def facture_print(buffer, factures):
    """ Draws the invoice """
    canvas = Canvas(buffer, pagesize=A4)
    lignes_per_page = 21

    for facture in factures:
        nb_lignes = facture.bons_livraison.count()  # Number of lines in the invoice
        page_total = math.ceil(nb_lignes / lignes_per_page)

        # Extraire le mois des bons de livraison
        mois_bons = []
        for bon_livraison in facture.bons_livraison.all():
            mois_bons.append(bon_livraison.date_livraison.strftime('%B %Y'))  # Extraire le mois en lettres

        # Pour éviter les doublons, utiliser un ensemble
        mois_unique = set(mois_bons)
        mois_affiche = ', '.join(mois_unique)  # Concaténer les mois s'il y a plusieurs

        for i in range(page_total):
            canvas.translate(0, 29.7 * cm)
            canvas.setFont('Helvetica', 9)

            canvas.saveState()
            draw_header(canvas, site=facture.client.site)
            canvas.restoreState()

            canvas.saveState()
            draw_footer(canvas, site=facture.client.site)
            canvas.restoreState()

            info_data_facture = [
                [u'FACTURE N° :', facture.numero],

            ]

            # Dessin des informations de la facture
            canvas.saveState()
            draw_document_info(canvas, info_data_facture, end_position=-6.5 * cm, font_size=200)
            canvas.restoreState()

            # Informations du client
            info_data_client = [
                [u'Client :', facture.client.nom],
                [u'Réf :', facture.client.external_id],
                [u'ICE :', facture.client.ice if facture.client.ice else '']
            ]





            canvas.saveState()
            canvas.translate(11 * cm, 0)  # Décaler vers la droite
            draw_info(canvas, info_data_client, end_position=-5.5 * cm)
            canvas.restoreState()

            info_data = [
                [facture.montant_lettres],
            ]

            canvas.saveState()
            draw_document_info(canvas, info_data, end_position=-27.8 * cm)
            canvas.restoreState()

            headers = [u'Date',u'Bon Livraison', u'Produit', u'Quantité', u'P.U TTC', u'Tax TVA', u'Montant TTC']
            data_to_print = []

            # Initialisation des montants pour chaque taux de TVA
            montant_ht_10 = 0
            montant_ht_20 = 0
            montant_tva_10 = 0
            montant_tva_20 = 0
            montant_ttc_10 = 0
            montant_ttc_20 = 0

            # Data collection
            for bon_livraison in facture.bons_livraison.all():
                for article in bon_livraison.articles.all():  # Parcours des articles liés au bon de livraison
                    product_name = article.article.nom  # Accède au nom du produit (via le modèle Produit)
                    date = bon_livraison.date_livraison
                    quantity = article.quantite
                    formatted_quantity = "{:.0f}".format(quantity)

                    tva = 10
                    tva_percentage = int(float(10))

                    price = article.article.prix  # Accède au prix du produit (via le modèle Produit)



                    tva_formatted = f"TVA {tva_percentage}%"
                    data_to_print.append(
                        [date, bon_livraison, product_name, formatted_quantity, price, tva_formatted,
                         ])



            # Calcul du total TTC général
            total_ttc = montant_ttc_10 + montant_ttc_20   # Ajout de la main d'œuvre

            # Création du dictionnaire des totaux pour chaque taux
            totals = {

            }

            canvas.saveState()
            draw_orderly_simple_table(canvas, headers, data_to_print,
                                      [2.3 * cm,6 * cm, 4 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 2 * cm, 2.2 * cm],
                                      lignes_per_page, expand_to_bottom=True, start_position=-7 * cm)
            canvas.restoreState()

            # Position pour le texte "Arrêté la présente facture à la somme de :"
            canvas.setFont('Helvetica-Bold', 10)
            position_y = -26.8 * cm  # Ajustez cette position en fonction de votre mise en page
            canvas.drawString(1 * cm, position_y, f"Arrêté la présente facture à la somme de :")

            canvas.saveState()
            # background_text(canvas, "FACTURE")  # Adjust the text as needed
            canvas.restoreState()



            # Displaying page numbers
            draw_page_nb(canvas, i + 1, page_total)
            canvas.showPage()

    canvas.save()


