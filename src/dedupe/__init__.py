import hashlib
import pathlib

import click


@click.command()
@click.argument("directory", type=click.Path(file_okay=False, dir_okay=True, exists=True), default=".")
@click.option("-y", "--yes", flag_value=True, default=False)
def main(directory, yes):
    where = pathlib.Path(directory)
    hashes = {}
    for path in where.iterdir():
        if not path.is_file(follow_symlinks=False):
            continue
        with open(path, "rb") as file:
            file_hash = hashlib.file_digest(file, hashlib.sha256).digest()
        if file_hash in hashes:
            delete = click.confirm(f"Delete \"{path}\"? (same as \"{hashes[file_hash]}\")", default=False) if not yes else True
            if delete:
                path.unlink(missing_ok=True)
            else:
                click.echo(f"Skipped \"{path}\"")
        hashes[file_hash] = path
