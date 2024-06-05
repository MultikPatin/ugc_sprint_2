from pydantic import BaseModel


class Review(BaseModel):
    title: str
    body: str
    created_at: str
    author: str
    movie: str

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class ReviewLike(BaseModel):
    review: str
    rating: int
    user: str

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class MovieLike(BaseModel):
    movie: str
    rating: int
    user: str

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class Bookmark(BaseModel):
    user: str
    movies: list[str]

    @classmethod
    def from_list(cls, tpl):
        tpl[1] = tpl[1].split(",")
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


SCHEMAS_MAPPING = {
    "bookmark": Bookmark,
    "movie_like": MovieLike,
    "review": Review,
    "review_like": ReviewLike
}