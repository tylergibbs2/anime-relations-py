# anime-relations-py

A parser for anime-relations. So you don't have to.

## Installation

```sh
$ pip install -U anime-relations-py
```

## Usage

```py
>>> from anime_relations_py import AnimeRelations

>>> parser = AnimeRelations()    # instance is empty until fetched
>>> parser.fetch_sync()          # alt: await parser.fetch_async()

>>> rule = parser.from_mal(40028)
>>> rule
Rule(mal_from=40028, kitsu_from=42422, anilist_from=110277, episodes_from=(60, 75), mal_to=40028, kitsu_to=42422, anilist_to=110277, episodes_to=(1, 16))
>>> rule.get_episode_redirect(65)
6
>>> rule.mal_to
40028
>>> parser.meta
{'version': '1.3.0', 'last_modified': '2021-02-25'}
```

For more advanced usage and other methods, please look at the source code. It's quite short and well-documented.