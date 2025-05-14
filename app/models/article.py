from datetime import datetime

class Article:
    def __init__(self, slug, title, description, image_path, category, publish_date, summary):
        self.slug = slug
        self.title = title
        self.description = description
        self.image_path = image_path
        self.category = category
        self.publish_date = publish_date
        self.summary = summary

    @property
    def category_style(self):
        """Renvoie la classe CSS correspondant à la catégorie"""
        category_styles = {
            'Histoire': 'bg-primary',
            'Conseils': 'bg-success',
            'Événement': 'bg-warning text-dark',
            'Équipement': 'bg-info'
        }
        return category_styles.get(self.category, 'bg-secondary')

def get_all_articles():
    """Renvoie la liste de tous les articles avec leurs métadonnées"""
    articles = [
        Article(
            slug='une_passion_nee',
            title='Une passion née pour le wingfoil',
            description='Découvrez comment est née la passion pour le wingfoil et comment cette aventure a mené à la création de Wing4All à Saint-Malo.',
            image_path='img/articles/actus/une_passion_née.jpeg',
            category='Histoire',
            publish_date=datetime(2025, 4, 1),
            summary='Découvrez comment est née ma passion pour le wingfoil et comment cette aventure m\'a mené à créer Wing4All.'
        ),
        Article(
            slug='preparation_du_matos',
            title='Préparation du matériel de wingfoil',
            description='Les étapes essentielles pour préparer votre matériel de wingfoil avant une session. Conseils pratiques d\'entretien.',
            image_path='img/articles/actus/prepaTest_matos.jpeg',
            category='Conseils',
            publish_date=datetime(2025, 4, 27),
            summary='Les étapes essentielles pour préparer votre matériel de wingfoil avant une session.'
        ),
        Article(
            slug='ouverture_de_wing4all',
            title='Ouverture officielle de Wing4All',
            description='L\'ouverture officielle de Wing4All, votre nouveau service de location de matériel de wingfoil à Saint-Malo.',
            image_path='img/articles/actus/ouverture.jpeg',
            category='Événement',
            publish_date=datetime(2025, 5, 1),
            summary='Découvrez l\'ouverture officielle de Wing4All, votre nouveau service de location de matériel de wingfoil.'
        ),
        Article(
            slug='reception_com',
            title='Réception du matériel Wing4All',
            description='Découverte du nouveau matériel de wingfoil fraîchement reçu pour Wing4All à Saint-Malo.',
            image_path='img/articles/actus/reception_com.jpeg',
            category='Équipement',
            publish_date=datetime(2025, 4, 20),
            summary='Découvrez le nouveau matériel de wingfoil fraîchement reçu pour Wing4All.'
        )
    ]
    return articles

def get_article_by_slug(slug):
    """Récupère un article par son slug"""
    articles = get_all_articles()
    for article in articles:
        if article.slug == slug:
            return article
    return None

def get_sorted_articles(reverse=True):
    """Renvoie la liste des articles triés par date de publication
    Par défaut: du plus récent au plus ancien"""
    articles = get_all_articles()
    return sorted(articles, key=lambda x: x.publish_date, reverse=reverse)