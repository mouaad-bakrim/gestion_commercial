from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
import math
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from base.pdf_utils import draw_page_nb, draw_footer,draw_info
from base.pdf_bc_utils import (
    draw_page_nb, draw_footer, draw_document_info, draw_orderly_simple_table, draw_header
)

def bon_de_livraison(buffer, commandes, utilisateur_nom, document_type):
    """ Draws the purchase order """
    canvas = Canvas(buffer, pagesize=A4)
    lignes_per_page = 8
    header_style = ParagraphStyle(name="header_centered", alignment=TA_CENTER, fontSize=10, fontName="Helvetica")

    for commande in commandes:
        produits = [article.article.nom for article in commande.articles.all()]  # List all articles in the order
        nb_lignes = len(produits)
        page_total = math.ceil(nb_lignes / lignes_per_page)

        for i in range(page_total):
            canvas.translate(0, 29.7 * cm)
            canvas.setFont('Helvetica', 4)

            site = commande.client.site

            if site:
                draw_header(canvas, site, document_type)
                draw_footer(canvas, site=site)

                info_data = [

                    [u'Référence bon :', commande.bon_livraison],

                    [u'Date :', commande.date_livraison],

                ]

            canvas.saveState()
            draw_document_info(canvas, info_data, end_position=-7 * cm)
            canvas.restoreState()

            # Informations du client
            info_data_client = [
                [u'Client :', commande.client.nom],
                [u'Réf :', commande.client.external_id],
                [u'ICE :', commande.client.ice if commande.client.ice else '']
            ]


            canvas.saveState()
            canvas.translate(11 * cm, 0)  # Décaler vers la droite
            draw_info(canvas, info_data_client, end_position=-6 * cm)
            canvas.restoreState()

            # Header of the table
            header = [
                Paragraph(u'Article', header_style),
                Paragraph(u'Quantité', header_style),
            ]

            data_to_print = []

            # Iterate over the articles for the BonLivraisonClinet
            for article in commande.articles.all():
                produit = article.article.nom
                unit = " "  # Default unit

                if article.quantite == int(article.quantite):
                    quantite_formatted = f"{int(article.quantite)}{unit}"  # Format as integer with unit
                else:
                    quantite_formatted = f"{article.quantite:.2f}{unit}"  # Format as decimal with unit

                quantity_paragraph = Paragraph(quantite_formatted, header_style)
                data_to_print.append([
                    produit.strip(),
                    quantity_paragraph,
                ])

            # Set column widths
            col_widths = [12 * cm, 7 * cm]

            # Draw the table
            canvas.saveState()
            draw_orderly_simple_table(
                canvas, header, data_to_print, col_widths, lignes_per_page,
                expand_to_bottom=True, start_position=-8.5 * cm
            )

            # Add page number
            draw_page_nb(canvas, i + 1, page_total)
            canvas.showPage()

    canvas.save()
