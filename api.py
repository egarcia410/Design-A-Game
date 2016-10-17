# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages

from models import User, Game, Score
from forms import (
  StringMessage,
  NewGameForm,
  GameForm,
  MakeMoveForm,
  UserGameForm,
  UserActiveGamesForms,
  HighScoreForms,
  UserRankingForms,
  HistoryGameForms)

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
        if not request.user_name:
            return StringMessage(message='Enter a Username')

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
        """Creates new game. Choose attempts between 1-25, default is 5"""
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
        """Makes a move between 1-25. Returns
        a game form with game information"""
        if len(request.urlsafe_game_key) != 51:
            raise endpoints.NotFoundException('Invalid Game Key!!!!!')

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user_key = Game.query(Game.user == game.user).get()
        score = Score.query(Score.user == user_key.user).get()
        # Creates a Score Model for the user if one does not exist
        if not score:
            game.user_score()
            game.put()

        score = Score.query(Score.user == user_key.user).get()

        # Check if game exists
        if not game:
            raise endpoints.NotFoundException('Game Does Not Exist')

        # Checks if game is already over
        if game.game_over:
            return game.to_form('Game already over!')

        # Checks if game is within limits of the board
        if request.guess < 1 or request.guess > 25:
            raise endpoints.NotFoundException(
                'Invalid Move, Outside Grid Boundaries'
            )

        # Checks for duplicate guesses
        for guesses in game.guesses:
            if guesses == request.guess:
                raise endpoints.NotFoundException(
                    'Already Guessed This Number'
                )

        # Last turn, Game Over
        if game.attempts_remaining == 1:
            game.attempts_remaining -= 1
            game.guesses.append(request.guess)
            game.game_over = True
            game.put()
            score.losses += 1
            score.percentage = score.victories/(score.victories + score.losses)
            score.put()
            return game.to_form('Game over!')

        game.attempts_remaining -= 1
        game.guesses.append(request.guess)

        # Guess the correct location of the ship
        if request.guess == game.ship_location:
            game.game_over = True
            game.put()
            score.victories += 1
            score.percentage = score.victories/(score.victories + score.losses)
            score.put()
            return game.to_form('You win!')

        if request.guess != game.ship_location:
            game.put()
            return game.to_form('You Missed!')

    @endpoints.method(request_message=UserGameForm,
                      response_message=UserActiveGamesForms,
                      path='user/games',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of a User's active games."""
        user = User.query(User.name == request.user_name).get()

        if not user:
            raise endpoints.NotFoundException('Invalid User!')

        if user:
            games = Game.query(Game.user == user.key).fetch()
            # Checks if the user has any games
            if games:
                # Iterates through games and checks if game_over == False
                # Shows only games that are not finished
                return UserActiveGamesForms(
                    items=[game.active_form('Time to make a move')
                            for game in games if game.game_over is False]
                )
            else:
                raise endpoints.NotFoundException('Game not found!')

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

        if game:
            # Checks if game is already finished
            if game.game_over is True:
                raise endpoints.NotFoundException('Game Is Already Over')
            else:
                game.key.delete()
                return StringMessage(message='Game Deleted!')
        else:
            raise endpoints.NotFoundException('Game Does Not Exist')

    @endpoints.method(response_message=HighScoreForms,
                      path='leaderboard',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns users high scores, Most wins"""
        scores = Score.query().order(-Score.victories).fetch(limit=5)
        return HighScoreForms(items=[score.high_scores() for score in scores])

    @endpoints.method(response_message=UserRankingForms,
                      path='ranking',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns users ranking, Percentage of Wins"""
        scores = Score.query().order(-Score.percentage).fetch(limit=5)
        return UserRankingForms(items=[score.user_rankings()
                                for score in scores])

    @endpoints.method(request_message=UserGameForm,
                      response_message=HistoryGameForms,
                      path='history',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Returns all users game history"""
        user = User.query(User.name == request.user_name).get()
        games = Game.query(Game.user == user.key).fetch()
        return HistoryGameForms(items=[game.history_form() for game in games])


api = endpoints.api_server([Battleship])
