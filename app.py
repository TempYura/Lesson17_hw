# app.py
from db_config import *
from db_models import Movie, Director, Genre
from db_schemas import MovieSchema, DirectorSchema, GenreSchema


# Схемы таблиц
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# Вьюшки
@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        """
        Возвращает список всех фильмов.
        Можно фильтровать по director_id и/или genre_id
        """

        args = request.args.to_dict()

        if not args:
            all_movies = Movie.query.all()
            return movies_schema.dump(all_movies), 200

        if len(args) == 1:
            if director_id := args.get("director_id"):
                movies = Movie.query.filter(Movie.director_id == director_id).all()
                return movies_schema.dump(movies), 200

            if genre_id := args.get("genre_id"):
                movies = Movie.query.filter(Movie.genre_id == genre_id).all()
                return movies_schema.dump(movies), 200

            return "Не известный аргумент. Используйте genre_id и/или director_id для фильтрации.", 404

        if len(args) == 2:
            if "genre_id" in args and director_id in args:
                movies = Movie.query.filter((Movie.genre_id == args.get("genre_id")) & (Movie.director_id == args.get("director_id"))).all()
                return movies_schema.dump(movies), 200

        return "Не известные аргументы. Используйте genre_id и/или director_id для фильтрации.", 404

    def post(self):
        """добавляет кино в фильмотеку"""
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()

        return "", 201


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        """возвращает подробную информацию о фильме"""
        movie = Movie.query.get(mid)

        if not movie:
            return "Не найдено", 404

        return movie_schema.dump(movie), 200

    def put(self, mid):
        """обновляет кино"""

        req_json = request.json

        movie = Movie.query.get(mid)

        if not movie:
            return "Не найдено", 404

        movie.id = req_json.get("id")
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204


    def delete(self, mid):
        """удаляет кино"""
        movie = Movie.query.get(mid)

        if not movie:
            return "Не найдено", 404

        db.session.delete(movie)
        db.session.commit()

        return "", 204


@directors_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        """возвращает всех директоров"""
        all_directors = Director.query.all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        """добавляет директора"""
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()

        return "", 201

@directors_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did):
        """возвращает подробную информацию о директоре"""
        director = Director.query.get(did)

        if not director:
            return "Не найдено", 404

        return director_schema.dump(director), 200

    def put(self, did):
        """обновляет директора"""

        req_json = request.json

        director = Director.query.get(did)

        if not director:
            return "Не найдено", 404

        director.id = req_json.get("id")
        director.name = req_json.get("name")


        db.session.add(director)
        db.session.commit()

        return "", 204


    def delete(self, did):
        """удаляет директора"""
        director = Director.query.get(did)

        if not director:
            return "Не найдено", 404

        db.session.delete(director)
        db.session.commit()

        return "", 204


@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        """возвращает список всех жанров"""
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        """добавляет жанр"""
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()

        return "", 201

@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid):
        """возвращает информацию о жанре с перечислением списка фильмов по жанру"""
        genre = Genre.query.get(gid)

        if not genre:
            return "Не найдено", 404

        return genre_schema.dump(genre), 200

    def put(self, gid):
        """обновляет жанр"""

        req_json = request.json

        genre = Genre.query.get(gid)

        if not genre:
            return "Не найдено", 404

        genre.id = req_json.get("id")
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 204


    def delete(self, gid):
        """удаляет жанр"""
        genre = Genre.query.get(gid)

        if not genre:
            return "Не найдено", 404

        db.session.delete(genre)
        db.session.commit()

        return "", 204


@app.errorhandler(404)
def not_found():
    return "Ничего не нашлось!"


if __name__ == '__main__':
    app.run(debug=True)
