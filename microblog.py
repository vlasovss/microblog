from app import create_app, db, cli
from app.models import Post, User

app = create_app()
app.cli.add_command(cli.translate_cli)
app.cli.add_command(cli.es_cli)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
    }