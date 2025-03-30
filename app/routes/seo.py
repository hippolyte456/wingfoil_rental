from flask import Blueprint, make_response, url_for, request
from datetime import datetime

bp = Blueprint('seo', __name__)

def generate_meta_tags(title, description, image=None, type='website'):
    """Retourne un dictionnaire de balises meta dynamiques avec Open Graph et Twitter Cards."""
    base_keywords = ['location wingfoil', 'Saint-Malo', 'activités nautiques', 'wing foil', 
                    'cours wingfoil', 'location wing', 'Bretagne', 'sports nautiques']
    
    meta_tags = {
        'title': f"{title} | Wing4All - Location Wingfoil Saint-Malo",
        'description': description,
        'keywords': ', '.join(base_keywords),
        'robots': 'index, follow',
        # Open Graph tags
        'og:title': title,
        'og:description': description,
        'og:type': type,
        'og:url': request.url,
        'og:site_name': 'Wing4All',
        'og:locale': 'fr_FR',
        # Twitter Card tags
        'twitter:card': 'summary_large_image',
        'twitter:title': title,
        'twitter:description': description,
    }
    
    if image:
        meta_tags['og:image'] = image
        meta_tags['twitter:image'] = image
    
    return meta_tags

def generate_structured_data(page_type, data):
    """Génère les données structurées Schema.org selon le type de page."""
    base_data = {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": "Wing4All",
        "url": request.url_root,
        "telephone": "+33652583862",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Saint-Malo",
            "addressRegion": "Bretagne",
            "addressCountry": "FR"
        }
    }
    
    if page_type == "Product":
        base_data.update({
            "description": data.get('description', ''),
            "image": data.get('image', ''),
            "offers": {
                "@type": "Offer",
                "price": str(data.get('price', '')),
                "priceCurrency": "EUR",
                "availability": "https://schema.org/InStock"
            }
        })
    elif page_type == "LocalBusiness":
        base_data.update({
            "description": "Location de matériel de wingfoil à Saint-Malo",
            "image": url_for('static', filename='img/logo/wing_dallE-removebg.png', _external=True),
            "priceRange": "€€",
            "openingHours": "Mo-Su 09:00-19:00"
        })
    
    return base_data

def generate_breadcrumbs(items):
    """Génère le balisage des fils d'Ariane pour Schema.org."""
    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    for position, item in enumerate(items, start=1):
        breadcrumb_list["itemListElement"].append({
            "@type": "ListItem",
            "position": position,
            "name": item['name'],
            "item": item['url']
        })
    
    return breadcrumb_list

@bp.route('/robots.txt')
def robots():
    """Génère un fichier robots.txt dynamique."""
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login/
Disallow: /register/
Disallow: /my-reservations/

Sitemap: {url_for('seo.sitemap', _external=True)}
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically"""
    pages = []
    # Liste des routes statiques avec leurs priorités
    routes = {
        'main.home': {'changefreq': 'daily', 'priority': '1.0'},
        'main.formules': {'changefreq': 'weekly', 'priority': '0.8'},
        'main.conseils': {'changefreq': 'weekly', 'priority': '0.7'},
        'equipment.equipment_list': {'changefreq': 'daily', 'priority': '0.9'},
        'main.contact': {'changefreq': 'monthly', 'priority': '0.6'}
    }
    
    # Ajout des routes statiques
    for route, info in routes.items():
        try:
            url = url_for(route, _external=True)
            pages.append({
                'loc': url,
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'changefreq': info['changefreq'],
                'priority': info['priority']
            })
        except Exception as e:
            continue  # Skip if route doesn't exist

    # Création du sitemap XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response 