# -*- coding: utf-8 -*-

def init_command_cli(app):
    from .init_db_cli import init_db
    app.cli.add_command(init_db)

    from .destroy_alembic_version_cli import destroy_alembic_version
    app.cli.add_command(destroy_alembic_version)

    from .destroy_migrations_cli import destroy_migrations
    app.cli.add_command(destroy_migrations)
