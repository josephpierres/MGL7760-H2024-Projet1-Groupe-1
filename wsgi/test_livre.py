# test_livre.py

from biblio.routes import get_cache_key, set_cache_key
from biblio import livre_to_dict
class TestLivreFunctions:
    def test_livre_to_dict(self):
        # Créez un objet Livre fictif pour le test
        book = {
            'id': 1,
            'titre': 'Mon livre',
            'description': 'Un super livre',
            'isbn': '1234567890',
            'annee_apparition': 2022,
            'image': 'image.jpg',
            'editeur': {
                'id': 10,
                'nom': 'Éditions XYZ'
            },
            'categories': [{'nom': 'Fiction'}, {'nom': 'Aventure'}],
            'auteurs': [{'nom': 'John Doe'}, {'nom': 'Jane Smith'}]
        }

        # Appelez la fonction à tester
        result = livre_to_dict(book)

        # Vérifiez que le dictionnaire résultant contient les clés attendues
        assert 'id' in result
        assert 'titre' in result
        # Ajoutez d'autres assertions pour les autres clés    
