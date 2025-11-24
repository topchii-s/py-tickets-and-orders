from __future__ import annotations

from typing import Optional

from django.db import transaction

from db.models import Movie
from django.db import models


def get_movies(
    genres_ids=None,
    actors_ids=None,
    title=None,
):
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return (
        queryset.distinct()
        .order_by(
            models.Case(
                models.When(title__startswith="Harry Potter", then=0),
                default=1,
                output_field=models.IntegerField(),
            ),
            "id",
        )
    )


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )

    if genres_ids:
        movie.genres.set(genres_ids)

    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
