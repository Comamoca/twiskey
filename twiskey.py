import tweepy
import os
import click

from dotenv import load_dotenv
from misskey import Misskey


def post_mk(mk, msg: str) -> None:
    mk.notes_create(text=msg + "\nTwitterより")
    print("Misskey: 投稿しました。")


def post_tw(api, msg: str) -> None:
    api.update_status(msg)
    print("Twitter: 投稿しました。")


@click.group()
def cli():
    pass


@cli.command(help="TwitterとMisskeyに同時投稿します。")
@click.argument("msg")
def post(msg: str) -> None:
    load_dotenv(".env")

    api_key = os.environ.get("APIKEY")
    api_key_secret = os.environ.get("APIKEY_SECRET")
    token = os.environ.get("ACCESS_TOKEN")
    access_token = os.environ.get("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(token, access_token)
    api = tweepy.API(auth)

    mk_token = os.environ.get("MISSKEY_TOKEN")
    mk = Misskey("misskey.04.si", mk_token)

    post_tw(api, msg)
    post_mk(mk, msg)


cli.add_command(post)

if __name__ == "__main__":
    cli()
