import boto3
import click
import yaml

from cookbook.backends.local_backend import LocalBackend
from cookbook.cookbook import Cookbook


@click.group()
@click.option('--target', default='tmp/cookbook', type=click.Path(exists=True, file_okay=False, writable=True))
@click.pass_context
def cli(ctx, target):
    ctx.ensure_object(dict)

    ctx.obj['cookbook'] = Cookbook(LocalBackend(target))


@cli.command()
@click.argument("recipe_file", type=click.File("rb"))
@click.pass_context
def save(ctx, recipe_file):
    recipe = yaml.load(recipe_file)
    click.echo(ctx.obj.get('cookbook').save(recipe))


@cli.command()
@click.argument("recipe_id")
@click.pass_context
def read(ctx, recipe_id):
    click.echo(ctx.obj.get('cookbook').read(recipe_id))


@cli.command()
@click.argument("id", type=click.File("rb"))
@click.pass_context
def delete(ctx, recipe_id):
    click.echo(ctx.obj.get('cookbook').delete(recipe_id))


@cli.command()
@click.pass_context
def list(ctx):
    click.echo(ctx.obj.get('cookbook').list())


@cli.command()
@click.pass_context
def dynamo(ctx):
    ddb = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-2')
    response = ddb.list_tables()
    print(response)


if __name__ == '__main__':
    cli({})
