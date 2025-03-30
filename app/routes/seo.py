from flask import Blueprint, make_response, url_for
from datetime import datetime

bp = Blueprint('seo', __name__)

@bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically"""
    pages = []
    # Liste des routes statiques
    static_routes = ['home', 'formules', 'conseils', 'equipment_list', 'contact']
    
    # Ajout des routes statiques
    for route in static_routes:
        url = url_for(route, _external=True)
        pages.append({
            'loc': url,
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        })
    
    # Page d'accueil avec priorité maximale
    pages.append({
        'loc': url_for('home', _external=True),
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'changefreq': 'daily',
        'priority': '1.0'
    })

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