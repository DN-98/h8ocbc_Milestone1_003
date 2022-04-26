from config import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.SmallInteger, nullable=False)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    department = db.Column(db.Text, nullable=False)
    movies = db.relationship(
        'Movie',
        backref = 'director', #backref untuk di panggil di schema MovieSchema
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movie.title)'
    )

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.Text, nullable=False)
    budget = db.Column(db.BigInteger)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Date, nullable=False)
    revenue = db.Column(db.BigInteger)
    title = db.Column(db.Text, nullable=False)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer, unique=True)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)

class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        load_instance = True
    
    director = fields.Nested("MovieDirectorSchema", default=None)

class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        load_instance = True
    
    movies = fields.Nested('DirectorMovieSchema', default=[], many=True)

class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()