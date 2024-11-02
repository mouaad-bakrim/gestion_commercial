import django_tables2 as tables
import re
from django_tables2 import TemplateColumn
class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        # Calculer le total en utilisant l'accessor pour chaque ligne
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class AmountSummingTemplateColumn(tables.TemplateColumn):
    column_total = 0

    def render(self, value, record,table, bound_column, **kwargs):
        # Extraire la partie numérique
        numeric_value = re.sub(r'[^\d.]', '', value)

        try:
            montant = float(numeric_value)
        except ValueError:
            montant = 0  # Valeur par défaut en cas d'échec

        # Ajouter au total
        self.column_total += montant

        # Rendre la valeur formatée pour l'affichage dans le tableau
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        # Rendre le total dans le pied de page
        return f"{self.column_total:.2f}"



class VolumeSummingTemplateColumn(tables.TemplateColumn):
    column_total = 0

    def render(self, value, record, table, bound_column, **kwargs):
        # Vérifier si la valeur n'est pas None avant de la convertir en float
        if value is not None:
            try:
                self.column_total += float(value)
            except ValueError:
                pass  # Ignorer les valeurs qui ne sont pas convertibles en float

        # Utiliser la méthode de rendu du parent avec les arguments requis
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        # Retourner le total arrondi dans le pied de page
        return f"{round(self.column_total, 1)}"




class AmountTemplateColumn(TemplateColumn):
    column_total = 0

    def render(self, value, record, table, bound_column, **kwargs):
        print(f"Rendering value: {value} (Type: {type(value)})")  # Debugging
        # Assurez-vous que 'value' est une chaîne ou un nombre
        if callable(value):
            value = value()

        if isinstance(value, (int, float)):
            montant = float(value)
        else:
            # Extraire la valeur numérique si c'est une chaîne
            numeric_value = re.sub(r'[^\d.]', '', str(value))
            montant = float(numeric_value) if numeric_value else 0

        # Ajouter au total
        self.column_total += montant

        # Rendre la valeur formatée pour l'affichage
        return f"{montant:.2f} DH"

    def render_footer(self, bound_column, table):
        # Afficher le total dans le pied de page
        return f"{self.column_total:.2f} DH"


class QuantiteTemplateColumn(tables.TemplateColumn):
    column_total = 0

    def render(self, value, record, table, bound_column, **kwargs):
        # Vérifier si la valeur n'est pas None avant de la convertir en float
        if value is not None:
            try:
                self.column_total += float(value)
            except ValueError:
                pass  # Ignorer les valeurs qui ne sont pas convertibles en float

        # Utiliser la méthode de rendu du parent avec les arguments requis
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        # Retourner le total arrondi dans le pied de page
        return f"{round(self.column_total, 1)}"

class AmountSummingColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        self.column_total = 0.0  # Initialiser à 0.0 pour être explicite
        super().__init__(*args, **kwargs)

    def render(self, record, table, value, bound_column, **kwargs):
        # Vérifiez si la valeur est un nombre avant de l'ajouter
        if value is not None:
            self.column_total += value
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        return f"{self.column_total:.2f}"  # Formatage à deux décimales

from decimal import Decimal

class AmountLavageTemplateColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        self.column_total = Decimal('0.00')  # Utiliser Decimal pour la précision
        super().__init__(*args, **kwargs)

    def render(self, record, table, value, bound_column, **kwargs):
        # Vérifiez si la valeur est un nombre avant de l'ajouter
        if value is not None:
            self.column_total += value
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        return f"{self.column_total:.2f}"
class AmountPessageTemplateColumn(tables.TemplateColumn):
    def __init__(self, *args, **kwargs):
        self.column_total = Decimal('0.00')  # Utiliser Decimal pour la précision
        super().__init__(*args, **kwargs)

    def render(self, record, table, value, bound_column, **kwargs):
        # Vérifiez si la valeur est un nombre avant de l'ajouter
        if value is not None:
            self.column_total += value
        return super().render(record, table, value, bound_column, **kwargs)

    def render_footer(self, bound_column, table):
        return f"{self.column_total:.2f}"
