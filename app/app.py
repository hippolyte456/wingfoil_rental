from . import create_app
from config import LOGO_PATH, CONTACT_EMAIL

app = create_app()

@app.context_processor
def inject_logo_path():
    return dict(LOGO_PATH=LOGO_PATH)

@app.context_processor
def inject_contact_email():
    return dict(CONTACT_EMAIL=CONTACT_EMAIL)

if __name__ == '__main__':
    app.run(debug=True)