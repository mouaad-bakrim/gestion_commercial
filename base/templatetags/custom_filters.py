from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key, None)  # Renvoie None si la clé n'existe pas
    return None  # Si le dictionnaire est None, retourne None
