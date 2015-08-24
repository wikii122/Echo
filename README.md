#Echo

Simple key-value store, used to keep data under unique token for short time.

## Protocol

- GET `/new` - generates free data ID.
- POST `/data/<id>` - creates entry for new data, with parameters.
- PUT `/data/<id>` - updates data state.
- DELETE `/data/<id>` - removes data from server.

Data should delete itself after 24 hours of inactivity.


