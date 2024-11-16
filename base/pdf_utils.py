from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Table
from PIL import Image
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from base.models import Societe, Site

def drawRightAlignedWrappedText(canvas, x, y, text, available_width, text_size):
    wrapped_text = textwrap.wrap(text, width=available_width)
    for line in wrapped_text:
        text_width = stringWidth(line, 'NotoSansBold', text_size)
        canvas.drawString(x - text_width, y, line)
def draw_header(canvas, site):
    """ Draws the invoice header """


    right_margin = 1 * cm
    page_width = A4[0]
    available_width = page_width - right_margin
    if site.societe_obj.logo:
        try:
            # Assurez-vous que `Societe.societe_obj.logo.path` est un chemin valide
            with Image.open(site.societe_obj.logo.path) as img:
                width, height = img.size
                ratio = width / height

            # Dessiner l'image dans le PDF
            canvas.drawInlineImage(site.societe_obj.logo.path, 1 * cm, -2.6 * cm, 2 * ratio * cm, 2 * cm)
            debut_text = (2 * ratio + 1.5) * cm
        except IOError:
            print(f"Erreur lors de l'ouverture de l'image: {site.societe_obj.logo.path}")

        # Autres codes pour dessiner le texte
    canvas.setStrokeColorRGB(0, 62 / 255, 97 / 255)  # bleu
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica-Bold', 20)
    canvas.drawString(17 * cm, -1.1 * cm, 'FACTURE')

    title_text_dict = {


    }



    # ------------------#
    business_details = (
        site.nom,
        site.adresse1,
        site.adresse2,
        site.ville,
    )

    canvas.setLineWidth(4)
    canvas.line(0, -3.25 * cm, 21.7 * cm, -3.25 * cm)



    canvas.setFont('Helvetica', 8)
    textobject = canvas.beginText(debut_text, -1.6 * cm)

    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def bottom_signature_table(canvas, signataires, signature_height=3.5 * cm):
    nb_signataires = len(signataires)
    if nb_signataires == 0:
        return
    bottom_data = [signataires, [""] * nb_signataires]
    bottom_table = Table(bottom_data, colWidths=[19 * cm / nb_signataires], rowHeights=[0.8 * cm, signature_height])
    bottom_table.setStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0.7, 0.7, 0.7)),
        ('LINEABOVE', (0, 0), (-1, 1), 1, (0.7, 0.7, 0.7)),
        ('LINEBEFORE', (0, 0), (-1, -4), 1, (0.7, 0.7, 0.7)),
        ('LINEAFTER', (-1, 0), (-1, -4), 1, (0.7, 0.7, 0.7)),
        ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])

    tw, th, = bottom_table.wrapOn(canvas, 15 * cm, 19 * cm)
    print(th / cm)
    bottom_table.drawOn(canvas, 1 * cm, -27.5 * cm)


def draw_document_info(canvas, info_data, end_position=-8 * cm):
    for i, lingne in enumerate(info_data):
        info_data[i] = [col + " " * 4 for col in lingne]

    info_table = Table(info_data)

    info_table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
    ])
    tw, th, = info_table.wrapOn(canvas, 5 * cm, 3 * cm)
    info_table.drawOn(canvas, 1 * cm, end_position)
def draw_info(canvas, info_data, end_position=-8 * cm):
    # Remplace les valeurs None par des chaînes vides
    for i, ligne in enumerate(info_data):
        info_data[i] = [(col if col is not None else '') + " " * 4 for col in ligne]

    info_table = Table(info_data)
    info_table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
    ])
    tw, th = info_table.wrapOn(canvas, 5 * cm, 3 * cm)
    info_table.drawOn(canvas, 1 * cm, end_position)

def draw_page_nb(canvas, page, page_total):
    # Client address
    canvas.drawString(18.3 * cm, -3 * cm, u"Page {0} / {1}".format(page, page_total))


def draw_footer(canvas, site, total_ttc_tva_10=None, total_tva_10=None):
    """ Dessine le pied de page avec les informations de TVA et totaux """

    # Ligne de séparation dans le pied de page
    canvas.setStrokeColorRGB(0, 62 / 255, 97 / 255)
    canvas.setLineWidth(4)
    canvas.line(0, -28 * cm, 21.7 * cm, -28 * cm)

    # Affichage des informations de note du site
    note = site.invoice_footer()
    canvas.setFont('Helvetica', 9)
    for l in range(len(note)):
        text_width = stringWidth(note[l], 'Helvetica', 9)
        textobject = canvas.beginText((21.7 * cm - text_width) / 2.0, (-28.5 - l * 0.5) * cm)
        textobject.textLine(note[l])
        canvas.drawText(textobject)

    # Afficher les montants total TTC et TVA si fournis
    if total_ttc_tva_10 is not None and total_tva_10 is not None:
        canvas.setFont('Helvetica', 10)
        x = 2 * cm
        y = -29.5 * cm

        canvas.drawString(x, y, f"Montant Total TTC (TVA 10%) : {total_ttc_tva_10:.2f} €")
        canvas.drawString(x, y - 1 * cm, f"Montant Total TVA (10%) : {total_tva_10:.2f} €")


def format_currency(amount, currency):
    if currency:
        return u"{0:.2f} {1}".format(amount, currency)


def draw_orderly_simple_table(canvas, headers, data_lines, col_widths, lignes_per_page, expand_to_bottom=True,
                              start_position=-9 * cm):
    data = [headers] + \
           data_lines


    if expand_to_bottom:
        data += [[''] * len(headers)] * (lignes_per_page - len(data_lines))

    table = Table(data, colWidths=col_widths)

    style = [
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Change from 10 to 9
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0.7, 0.7, 0.7)),
        ('LINEBELOW', (0, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('LINEABOVE', (0, 0), (-1, 1), 1, (0.7, 0.7, 0.7)),
        ('LINEBEFORE', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ROWHEIGHT', (0, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2.2),


        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ]

    for i in range(1, len(data_lines) + 1):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), (0.9, 0.9, 0.9)))

    table.setStyle(style)

    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
    table.drawOn(canvas, 1 * cm, start_position - th)


# Create a reportlab function that writes text in the background of a page (useful for watermarks)
def background_text(canvas, text):
    canvas.setFont('Helvetica', 64)
    canvas.setFillColorRGB(0.9, 0.9, 0.9, 0.5)
    canvas.rotate(45)
    canvas.drawCentredString(-4 * cm, -19 * cm, text)
    canvas.rotate(-45)
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def draw_summary_table(canvas, totals, start_position=-8 * cm, end_position=-10 * cm):
    # Structure des données pour les taux de TVA à 10 % et 20 %
    summary_data_1 = [
        ['Taux de TVA', '10%', '20%'],  # En-tête pour les pourcentages de TVA
        ['Montant TTC', format_currency(totals['montant_ttc_10'], 'DH'),
         format_currency(totals['montant_ttc_20'], 'DH')],
        ['Montant HT', format_currency(totals['montant_ht_10'], 'DH'), format_currency(totals['montant_ht_20'], 'DH')],
        ['TVA', format_currency(totals['montant_tva_10'], 'DH'), format_currency(totals['montant_tva_20'], 'DH')],
    ]

    # Structure pour le tableau récapitulatif avec condition sur la main d'œuvre
    summary_data_2 = []

    # Ajouter le montant total TTC, qui inclut ou non la main d'œuvre
    summary_data_2.append(['Montant Total TTC', format_currency(totals['total_ttc'], 'DH')])

    # Création des tables
    summary_table_1 = Table(summary_data_1, colWidths=[9 * cm, 5 * cm, 5 * cm])  # Ajuster les largeurs des colonnes
    summary_table_2 = Table(summary_data_2, colWidths=[9 * cm, 10 * cm])  # Ajuster les largeurs des colonnes

    # Style pour la première table
    summary_table_1.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Change from 10 to 9
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])

    # Style pour la deuxième table
    summary_table_2.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.9, 0.9, 0.9)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all cells in the table
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])

    # Dessiner la première table sur le canvas
    tw1, th1 = summary_table_1.wrapOn(canvas, 15 * cm, 3 * cm)
    summary_table_1.drawOn(canvas, (canvas._pagesize[0] - tw1) / 2, start_position - th1)  # Centering the first table

    # Dessiner la deuxième table sur le canvas, positionnée en dessous de la première
    tw2, th2 = summary_table_2.wrapOn(canvas, 2 * cm, 3 * cm)
    summary_table_2.drawOn(canvas, (canvas._pagesize[0] - tw2) / 2,
                           start_position - th1 - th2 - 0 * cm)  # Centering the second table
