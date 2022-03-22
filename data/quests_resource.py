from flask import jsonify
from flask_restful import Resource
from flask_restful import abort

from data import db_session
from data.quests import Quest
from data.reqparse import parser


class QuestResource(Resource):
    def get(self, quest_id):
        abort_if_quests_not_found(quest_id)
        session = db_session.create_session()
        quest = session.query(Quest).get(quest_id)
        return jsonify({'quests': quest.to_dict(
            only=('content'))})

    def delete(self, quest_id):
        abort_if_quests_not_found(quest_id)
        session = db_session.create_session()
        quest = session.query(Quest).get(quest_id)
        session.delete(quest)
        session.commit()
        return jsonify({'success': 'OK'})


class QuestListResource(Resource):
    def get(self):
        session = db_session.create_session()
        quest = session.query(Quest).all()
        print(quest)
        for i in quest:
            print(i.content)
        return jsonify({'quest': [item.to_dict(
            only=('content')) for item in quest]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        quests = Quest(
            content=args['content'],
            user_id=args['user_id'],
            news_id=args['news_id']
        )
        session.add(quests)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_quests_not_found(quest_id):
    session = db_session.create_session()
    quests = session.query(Quest).get(quest_id)
    if not quests:
        abort(404, message=f"Quests {quest_id} not found")
