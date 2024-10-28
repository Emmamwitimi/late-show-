# routes.py
from flask import request, jsonify
from flask_restful import Resource, Api
from models import Episode, Guest, Appearance
from db import db  # Ensure you're importing db correctly

# Initialize API without needing to import app
api = Api()  # Initialize the API without passing app here

# Guest Resource with CRUD operations
class GuestsResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return jsonify([{
            "id": g.id,
            "name": g.name,
            "occupation": g.occupation
        } for g in guests])

    def post(self):
        data = request.get_json()
        new_guest = Guest(
            name=data.get('name'),
            occupation=data.get('occupation')
        )
        db.session.add(new_guest)
        db.session.commit()
        return jsonify({
            "id": new_guest.id,
            "name": new_guest.name,
            "occupation": new_guest.occupation
        }), 201

    def put(self, id):
        guest = Guest.query.get(id)
        if not guest:
            return jsonify({"error": "Guest not found"}), 404
        data = request.get_json()
        guest.name = data.get('name', guest.name)
        guest.occupation = data.get('occupation', guest.occupation)
        db.session.commit()
        return jsonify({
            "id": guest.id,
            "name": guest.name,
            "occupation": guest.occupation
        })

    def delete(self, id):
        guest = Guest.query.get(id)
        if not guest:
            return jsonify({"error": "Guest not found"}), 404
        db.session.delete(guest)
        db.session.commit()
        return jsonify({"message": "Guest deleted"}), 204

# Episode Resource for GET operations
class EpisodesResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        return jsonify([{
            'id': e.id,
            'date': e.date,
            'number': e.number
        } for e in episodes])

class EpisodeDetailResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return jsonify({"error": "Episode not found"}), 404

        return jsonify({
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": [{
                "episode_id": app.episode_id,
                "guest": {
                    "id": app.guest.id,
                    "name": app.guest.name,
                    "occupation": app.guest.occupation
                },
                "guest_id": app.guest_id,
                "id": app.id,
                "rating": app.rating
            } for app in episode.appearances]
        })

# Appearance Resource for POST operation
class AppearancesResource(Resource):
    def post(self):
        data = request.get_json()

        # Validate rating
        if not (1 <= data['rating'] <= 5):
            return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

        appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )

        db.session.add(appearance)
        db.session.commit()

        return jsonify({
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {
                "date": appearance.episode.date,
                "id": appearance.episode.id,
                "number": appearance.episode.number
            },
            "guest": {
                "id": appearance.guest.id,
                "name": appearance.guest.name,
                "occupation": appearance.guest.occupation
            }
        }), 201

# Add resources to API
api.add_resource(GuestsResource, '/guests', '/guests/<int:id>')
api.add_resource(EpisodesResource, '/episodes')
api.add_resource(EpisodeDetailResource, '/episodes/<int:id>')
api.add_resource(AppearancesResource, '/appearances')

# Initialize the API with the app
def init_app(app):
    api.init_app(app)  # This method initializes the API with the app
