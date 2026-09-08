from . import warn
from . import ban
from . import kick
from . import clear
from . import logs


def setup(tree, db):

    warn.setup(tree, db)
    ban.setup(tree)
    kick.setup(tree)
    clear.setup(tree)
    logs.setup(tree)