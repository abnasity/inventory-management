from app import create_app, db
from app.models import User, Device, Sale

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Add database models to flask shell context"""
    return {
        'db': db,
        'User': User,
        'Device': Device,
        'Sale': Sale
    }

if __name__ == '__main__':
    app.run(debug=True)