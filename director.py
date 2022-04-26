from flask import make_response, abort
from config import db
from models import Director, DirectorSchema

director_schema = DirectorSchema()
director_schema_many = DirectorSchema(many = True)

def read_all():
    """
    This function responds to a request for /api/directors
    with the complete lists of directors

    :return:        json string of list of directors
    """
    director = Director.query.limit(1000).all()
    data = director_schema_many.dump(director)
    return data, 200

def read_one(id):
    """
    This function responds to a request for /api/directors/{id}
    with one matching director from directors

    :param id:  Id of director to find
    :return:    director matching id
    """
    director = Director.query.filter(Director.id == id).one_or_none()
    if director is None:
        abort(404, f"director id = {id} has not found")
    else:
        data = director_schema.dump(director)
        return data, 200

def read_byName(name):
    """
    This function responds to a request for /api/directors/{name}
    with one matching director from directors

    :param name:  name of director to find
    :return:    director who have name like %{name}%
    """
    directors = Director.query.filter(Director.name.ilike(f"%{name}%")).all()

    if directors is not None:
        data = director_schema_many.dump(directors)
        return data, 200
    else:
        abort(404, f"in director list There is no director having name Like %{name}%")

def create(director):
    """
    This function creates a new director in the directors structure
    based on the passed in director data

    :param director:  director to create in directors structure
    :return:        201 on success, 409 on director exists
    """
    uid = director.get("uid")
    exist_director = Director.query.filter(Director.uid == uid).one_or_none()

    if exist_director is None:
        new_director = director_schema.load(director, session=db.session)

        db.session.add(new_director)
        db.session.commit()

        data = director_schema.dump(new_director)
        return data, 201
    else:
        abort(409, f"director with uid = {uid} already exist")

def update(id, director):
    """
    This function updates an existing director in the directors structure

    :param id:          Id of the director to update in the directors structure
    :param director:    director to update
    :return:            200 on success and updated data director structure, 404 if director not found
    """
    update_director = Director.query.filter(Director.id == id).one_or_none()

    if update_director is None:
        abort(404, f"director with id = {id} has not found")
    else:
        update = director_schema.load(director, session=db.session)

        update.id = update_director.id

        db.session.merge(update)
        db.session.commit()

        data = director_schema.dump(update)
        return data, 200

def delete(id):
    """
    This function deletes a director from the directors structure

    :param id:   Id of the director to delete
    :return:     200 on successful delete, 404 if not found
    """
    director = Director.query.filter(Director.id == id).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f'Successfully delete director with id = {id}', 200)
    else:
        abort(404, f"director with id {id} has not found")