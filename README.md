# Battleship Game API
###### Udacity's Full Stack Web Developer Nanodegree
----
## Set-Up Instructions:
1.  Download the Google App Engine [here](https://cloud.google.com/appengine/docs/python/download)
2.  Git clone the project [here](https://github.com/egarcia410/Design-A-Game.git)
3.  Add the newly cloned project as an 'Add Existing Application' to the GoogleAppEngineLauncher
4.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console.
5.  Run the app from the GoogleAppeEngineLauncher
6.  Inside your browser go to localhost:8080/_ah/api/explorer. (default is localhost:8080)

## Game Description:
This is a simple battleship game for 1 player. Once, a user is created, you can create a new game. Each new game will generate a 5x5 grid with 1 ship (1 cell size) randomly placed within the grid. The player can change the number of attempts between 1-25, default is 5. The game is won once the player guesses correctly the location of the ship or runs out of attempts to guess.

## Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for cron, email notification
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

## Endpoints Included:

 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will
    raise an error if a User with that user_name already exists.


 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Attempts value must be between 1-26.


 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Urlsafe_game_key is required and will be validated. Guesses must be valid, or a message will appear that the number is outside the grid. Each guess will display the outcome of the guess(hit, miss, or game over) Once the game is over, the results will be stored in the Score Model.


 - **get_user_games**
    - Path: 'user/games'
    - Method: GET
    - Parameters: UserGameForm(user_name)
    - Returns: UserActiveGamesForms
    - Description: Returns all Users active games.


 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms.
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.


 - **cancel_game**
    - Path: 'game/cancel/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: StringMessage
    - Description: Requires a valid urlsafe_game_key. Cancels a game that is in progess. Games that are finsihed can't be deleted.


 - **get_high_scores**
    - Path: 'leaderboard'
    - Method: GET
    - Parameters: None
    - Returns: HighScoreForms
    - Description: Returns the top 5 players by total of wins in descending order.


 - **get_user_rankings**
    - Path: 'ranking'
    - Method: GET
    - Parameters: None
    - Returns: UserRankingForms
    - Description: Returns the top 5 players by win percentage in descending order.


 - **get_game_history**
    - Path: 'history'
    - Method: GET
    - Parameters: UserGameForm (user_name)
    - Returns: HistoryGameForms
    - Description: Returns all users game results.

## Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.

## Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining, guesses, rows, game_over, message, user_name).
 - **UserGameForm**
    - Input Field (user_name) for retreiving user's game history and active games.
 - **UserActiveGamesForm**
    - Information about a users active games.
 - **UserActiveGamesForms**
    -  Returns UserActiveGamesForms.
 - **NewGameForm**
    - Input Field (user_name, attempts) used to make a new game request.
 - **MakeMoveForm**
    -  Input Field (guess) used to make a move in an existing game.
 - **HighScoreForm**
    -  Information about the users with the most wins.
 - **HighScoreForms**
    - Returns HighScoreForm.
 - **UserRankingForm**
    - Infomation about the users with the best winning percentage.
 - **UserRankingForms**
    - Returns UserRankingForm.
 - **HistoryGameForm**
    - Infomation about a users game history.
 - **HistoryGameForms**
    - Returns HistoryGameForm.
 - **StringMessage**
    - General purpose String container.