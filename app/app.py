from . import create_app
from config import LOGO_PATH

app = create_app()

@app.context_processor
def inject_logo_path():
    return dict(LOGO_PATH=LOGO_PATH)

if __name__ == '__main__':
    app.run(debug=True)