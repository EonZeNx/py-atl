from py_atl.database import DB_CONNECTION
from ApexToolsLauncher.Core.Hash import HashDatabase, EHashType


def lookup(game_hash: int):
    if DB_CONNECTION is None:
        return None

    return DB_CONNECTION.Lookup(game_hash)


def lookup_filepath(game_hash: int):
    if DB_CONNECTION is None:
        print(f"lookup_filepath : DB_CONNECTION is None")
        return None

    return DB_CONNECTION.Lookup(game_hash, EHashType.FilePath)
