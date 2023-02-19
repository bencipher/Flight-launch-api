import os
from .factory import create_app

app = create_app()

if __name__ == "__main__":
    config_name = os.getenv('FLASK_ENV', 'prod')
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=5000)
