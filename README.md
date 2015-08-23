#Echo

Simple echoserver, designed for TTR app.

## Protocol

- GET `/new` - generates free game ID.
- POST `/game/<id>` - creates entry for new game, with parameters.
- PUT `/game/<id>` - updates game state.
- DELETE `/game/<id>` - removes game from server.

Game should delete itself after 24 hours of inactivity.


