import os

import click
from flask.cli import AppGroup

from app.models import Post

translate_cli = AppGroup('translate')
es_cli = AppGroup('elastic')


@translate_cli.command('init')
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate_cli.command('update')
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate_cli.command('compile')
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@es_cli.command('reindex')
@click.argument('post')
def reindex(post):
    """Reindex model Post for ES."""
    try:
        Post.reindex()
    except:
        raise RuntimeError('Reindex model Post - commmand failed')