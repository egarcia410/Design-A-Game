# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms, UserGameForm, UserActiveGamesForm, UserActiveGamesForms,\
    HighScoreForms, HighScoreForm, UserRankingForms, UserRankingForm,\
    GameHistoryForms
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


@endpoints.api(name='battleship', version='v1')
class Battleship(remote.Service):
    """Battleship API"""


    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))


    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game. Choose attempts between 1-10, default is 5"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        if request.attempts < 1:
            raise endpoints.NotFoundException(
                    'Attempts Remaining needs to be more than 0')
        if request.attempts > 26:
            raise endpoints.NotFoundException(
                    'Attempts Remaining needs to be less than 26')
        game = Game.new_game(user.key, request.attempts)

        return game.to_form('Good luck playing Battleship!')


    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move between 1-25. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user_key = Game.query(Game.user == game.user).get()
        user = User.query(User.key == user_key.user).get()
        if game.game_over:
            return game.to_form('Game already over!')
        if request.guess < 1 or request.guess > 25:
            raise endpoints.NotFoundException('Invalid Move, Outside Grid Boundaries')
        for guesses in game.guesses:
            if guesses == request.guess:
              raise endpoints.NotFoundException('Already Guessed This Number')

        if game.attempts_remaining < 1:
            game.game_over = False
            user.losses += 1
            user.percentage = user.victories/(user.victories + user.losses)
            user.put()
            return game.to_form('Game over!')

        game.attempts_remaining -= 1
        game.guesses.append(request.guess)

        if request.guess == game.ship_location:
            game.game_over = True
            user.victories += 1
            user.percentage = user.victories/(user.victories + user.losses)
            game.put()
            user.put()
            return game.to_form('You win!')

        if request.guess != game.ship_location:
            game.put()
            user.put()
            return game.to_form('You Missed!')

# #  Fix this!
# TypeError: 'Game' object is not iterable
    @endpoints.method(request_message=UserGameForm,
                      response_message=UserActiveGamesForms,
                      path='user/games',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of a User's active games."""
        user = User.query(User.name == request.user_name).get()
        # works if .get() is used instead of fetch()
        #fetch will retrieve list
        games = Game.query(Game.user == user.key).get()
        # if games.game_over == False:
        #   return games.active_form('Time to make a move!')
        if games:
            return UserActiveGamesForms(items=[games.active_form('Time to make a move') for game in games])
        else:
            raise endpoints.NotFoundException('Game not found!')
        # return StringMessage(message=games)


    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/cancel/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='GET')
    def cancel_game(self, request):
        """Delete a game in progress"""
        if len(request.urlsafe_game_key) != 51:
          raise endpoints.NotFoundException('Invalid Game Key!!!!!')

        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        # Check if game exists
        if not game:
          raise endpoints.NotFoundException('Game Does Not Exist')

        # Checks if game is already finished
        if game.game_over:
          raise endpoints.NotFoundException('Game Is Already Over')

        game.key.delete()
        return StringMessage(message='Game Deleted!')


# Fix Order!
    @endpoints.method(response_message=HighScoreForms,
                      path='leaderboard',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns users high scores, Most wins"""
        users = User.query()
        users.order(User.victories).fetch(10)
        return HighScoreForms(items=[user.high_scores() for user in users])


# Fix order!
    @endpoints.method(response_message=UserRankingForms,
                      path='ranking',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns users ranking, Percentage of Wins"""
        users = User.query()
        # order fix... :'(
        users.fetch(limit=1)
        return UserRankingForms(items=[user.user_rankings() for user in users])


# Fix this!
# TypeError: 'Game' object is not iterable
    @endpoints.method(request_message=UserGameForm,
                      response_message=GameHistoryForms,
                      path='history',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Returns all users game history"""
        user = User.query(User.name == request.user_name).get()
        games = Game.query(Game.user == user.key).fetch()
        # return games.history_form()
        return GameHistoryForms(items=[game.history_form() for game in games])
        # return StringMessage(message=games)


api = endpoints.api_server([Battleship])
