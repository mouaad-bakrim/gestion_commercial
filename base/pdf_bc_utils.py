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
def draw_header(canvas, site, document_type):
    """ Draws the invoice header """


    right_margin = 1 * cm
    page_width = A4[0]

    available_width = page_width - right_margin
    debut_text = 8 * cm
    if Site.objects.first().societe_obj.logo:
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

        if document_type == 'bon_de_commande':
            header_text = 'Bon de Commande'
        elif document_type == 'bon_de_reception':
            header_text = 'Bon de Réception'
        elif document_type == 'bon_de_livrasion':
            header_text = 'Bon de Livraision'


        else:
            raise ValueError("Type de document inconnu.")

            # Dessiner le texte de l'en-tête
        canvas.setStrokeColorRGB(0.92, 0.635, 0.051)

        canvas.setFillColorRGB(0.2, 0.2, 0.2)
        canvas.setFont('Helvetica-Bold', 20)
        canvas.drawString(14 * cm, -1.1 * cm, header_text)

    title_text_dict = {
        'fact': 'FACTURE',

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



    canvas.setFont('Helvetica', 10)
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
        ('FONTSIZE', (0, 0), (-1, -1), 9),
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


def draw_document_info(canvas, info_data, end_position):
    for i, lingne in enumerate(info_data):
        # Utilisation d'une vérification pour None
        info_data[i] = [col if col is not None else "" + " " * 4 for col in lingne]

    info_table = Table(info_data)

    info_table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, -1), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
    ])
    tw, th, = info_table.wrapOn(canvas, 5 * cm, 3 * cm)
    info_table.drawOn(canvas, 1 * cm, end_position)


def draw_page_nb(canvas, page, page_total):
    # Client address
    canvas.drawString(18.3 * cm, -3 * cm, u"Page {0} / {1}".format(page, page_total))


def draw_footer(canvas, site):
    """ Draws the invoice footer """

    canvas.setStrokeColorRGB(0.92, 0.635, 0.051)
    canvas.setLineWidth(4)
    canvas.line(0, -28 * cm, 21.7 * cm, -28 * cm)

    note = site.invoice_footer()
    canvas.setFont('Helvetica', 9)
    for l in range(len(note)):
        text_width = stringWidth(note[l], 'Helvetica', 9)
        textobject = canvas.beginText((21.7 * cm - text_width) / 2.0, (-28.5 - l * 0.5) * cm)
        textobject.textLine(note[l])
        canvas.drawText(textobject)
    canvas.setFont('Helvetica', 10)


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
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0.7, 0.7, 0.7)),
        ('LINEBELOW', (0, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('LINEABOVE', (0, 0), (-1, 1), 1, (0.7, 0.7, 0.7)),
        ('LINEBEFORE', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8))  # Bleu clair

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


def draw_summary_table(canvas, totals, start_position=-8 * cm):
    summary_data = [
    ]

    summary_table = Table(summary_data, colWidths=[16 * cm, 3 * cm])
    summary_table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])

    tw, th = summary_table.wrapOn(canvas, 15 * cm, 3 * cm)
    summary_table.drawOn(canvas, 1 * cm, start_position - th)