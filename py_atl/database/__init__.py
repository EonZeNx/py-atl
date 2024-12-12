from ApexToolsLauncher.Core.Hash import HashDatabase, EHashType

DB_CONNECTION = None


def setup(db_path: str) -> None:
    global DB_CONNECTION

    if DB_CONNECTION is not None:
        return

    option_database = HashDatabase.Create(db_path)
    if option_database.IsNone:
        print(f"failed to setup hash database")
        return

    DB_CONNECTION = option_database.Unwrap()
    DB_CONNECTION.OpenConnection()


def setup_jc3() -> None:
    from os import path
    from py_atl import addon

    setup(path.join(addon.project_path(), "database", "atl.jc3.db"))


def lookup(game_hash: int):
    global DB_CONNECTION

    if DB_CONNECTION is None:
        print(f"lookup_filepath : DB_CONNECTION is None")
        return None

    return DB_CONNECTION.Lookup(game_hash)


def lookup_filepath(game_hash: int):
    global DB_CONNECTION

    if DB_CONNECTION is None:
        print(f"lookup_filepath : DB_CONNECTION is None")
        return None

    return DB_CONNECTION.Lookup(game_hash, EHashType.FilePath)
