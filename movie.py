from flask import make_response, abort
from config import db
from models import Movie, MovieSchema,  Director

movie_schema = MovieSchema()
movie_schema_many = MovieSchema(many = True)

def read_all():
    """
    This function responds to a request for /api/movies
    with the complete lists of movies

    :return:    json string of list of movies
    """
    movie = Movie.query.limit(500).all()
    data = movie_schema_many.dump(movie)
    return data, 200

def read_one(id):
    """
    This function responds to a request for /api/movies/{id}
    with one matching movie from movies

    :param id:  Id of movie to find
    :return:    movie matching id
    """
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    
    if movie is not None:
        data = movie_schema.dump(movie)
        return data, 200
    else:
        abort(404, f"Movie with id = {id} has not found")

def read_byTitle(title):
    """
    This function responds to a request for /api/movies/{title}
    with matching title of movie from movies

    :param title:  title of movie to find
    :return:    movie who have title like %{title}%
    """
    movies = Movie.query.filter(Movie.title.ilike(f"%{title}%")).all()

    if movies is not None:
        data = movie_schema_many.dump(movies)
        return data, 200
    else:
        abort(404, f"in movie list There is no movie having title Like %{title}%")

def create(director_id, movie):
    """
    This function creates a new movie in the movies structure
    based on the passed in director_id and movie data

    :param director_id: movie director id
    :param movie:       movie to create in movies structure
    :return:            201 on success, 409 on movie uid exists, 404 on movie director doesn't exist
    """
    uid = movie.get("uid")
    exist_movie = Movie.query.filter(Movie.uid == uid).one_or_none()
    exist_director = Director.query.filter(Director.id == director_id).one_or_none()

    if exist_director is None:
        abort(404, f"director not found")
    
    if exist_movie is None:
        new_movie = movie_schema.load(movie, session=db.session)
        new_movie.director_id = director_id

        db.session.add(new_movie)
        db.session.commit()

        data = movie_schema.dump(new_movie)
        return data, 201
    else:
        abort(409, f"movie with uid {uid} already exist")

def update(id, movie):
    """
    This function updates an existing movie in the movies structure

    :param id:          Id of the movie to update in the movies structure
    :param movie:       movie to update
    :return:            200 on success and updated data movie structure, 404 if movie not found
    """
    update_movie = Movie.query.filter(Movie.id == id).one_or_none()

    if update_movie is not None:
        update = movie_schema.load(movie, session=db.session)
        update.id = update_movie.id

        db.session.merge(update)
        db.session.commit()

        data = movie_schema.dump(update)
        return data, 200
    else:
        abort(404, f"movie with id = {id} has not found")

def delete(id):
    """
    This function deletes a movie from the movies structure

    :param id:   Id of the movie to delete
    :return:     200 on successful delete, 404 if not found
    """
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(f'Successfully delete director with id = {id}', 200)
    else:
        abort(404, f"movie with id {id} has not found")