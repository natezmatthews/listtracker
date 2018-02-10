from app import app, db
from app.models import Risuto, Item, Separator

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Risuto': Risuto,
            'Item': Item,
            'Separator':Separator
           }