import json
import os



def file_writer(obj, filepath):
    import os
    import json

    # S'assurer que le fichier existe
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)

    try:
        data = file_reader(filepath)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    # Préparation des données à écrire
    if isinstance(obj, list):
        # Vérifie si les éléments sont des objets ou déjà des dicts
        for item in obj:
            if hasattr(item, 'to_dict'):
                data.append(item.to_dict())
            elif isinstance(item, dict):
                data.append(item)
            else:
                raise TypeError("Les éléments de la liste doivent être des objets avec 'to_dict' ou des dictionnaires.")
    else:
        # Cas d'un seul objet
        if hasattr(obj, 'to_dict'):
            data.append(obj.to_dict())
        elif isinstance(obj, dict):
            data.append(obj)
        else:
            raise TypeError("L'objet doit avoir une méthode 'to_dict' ou être un dictionnaire.")

    # Sauvegarde finale
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def file_reader(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return []
    
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Erreur de lecture du fichier {filepath}. Il est probablement vide ou mal formé.")
            return []
        
def file_reset(filepath):
    with open(filepath, "w") as f:
        json.dump([], f)