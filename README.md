**Initial test practicing using RESTful APIs.**

1. Input
> Raw data: 1k+ lines of nested JSON from the dining API (menus, stations, items, attributes, hours, events).

2. Goals
> - Parse and understand the nested JSON <br>
> - Identify key entities: Meal, Station, Item <br>

3. Behavior
> - fetch the menu based on user input of:  
> - period (breakfast, lunch, dinner) <br>
> - date (enter year, month, and day) <br>
<br><br>
**Potential next improvements**
  Implementing a DAO instead of using function defintions (methods) would be more architecturally sound. <br>
  Also, using objects rather than simple lists would improve readability. <br>
  Finally, many of the parsing and fetching of intitial data coudld benefit from seperation (different classes / files.) <br>
  Some parameters are hardcoded, this can be optimized as well.  <br>

However, this project was meant to be an introductury activity so I can become more familiar with REST APIs.
<br><br>
<br>
**Further improvement plan, if I ever return to this project:**
<br>Identify key entities: Meal, Station, Item, Attribute, Hall, Hours, Event. <br> 
Map relationships (e.g., a Meal has multiple Stations, a Station has multiple Items).<br>
Design a data model based on the above <br>

**Possibly?? Include relationships and relevant fields (allergens, macros, availability, dates).**
<br> Build backend architecture

**have functions or services that call the API and populate your models.**
<br>Optional persistence: save parsed data to JSON, CSV, or a database.

**Implement business logic**
<br>Filters: by meal period, favorites.
Aggregations: daily menus, totals for macros.<br>
Event-based logic: notifications when meals are available or halls are closing.<br>
Anything derived: favorites tracking, meal suggestions, or alerts.

**Deliverable**
<br>A backend system that can:
Query the API or cached data<br>
Produce structured, usable objects (Meal → Station → Item → Attributes)<br>
Perform operations and queries on that data efficiently<br>
Provide relevant updates for users.
