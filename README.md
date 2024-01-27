# CSC370 - Database Systems
Coursework from CSC 370 at UVic (Summer 2023)

This course gives an overview of relational database management systems (RDBMS's), a foundational tool in data management, including how to model the world with relational schemata, extract and analyse data with declarative query languages, and design data-powered applications.

Topics:
1. Relational Data Analysis:
    - Writing, debugging, and simplifying SQL DQL queries
  - Connecting to and querying a relational database from application code
  - Analysing query performance empirically and within the I/O model of computation in order to select appropriate indexes to accelerate the query
2. Data Modelling:
  - Constructing and evaluating Entity-Relationship Diagrams (ERD's) to model requirements as data with extensibility in mind
  - Analytically converting relations into Boyce-Codd, Third, and/or Fourth normal forms
  - Implementing constraints and triggers to maintain consistency of state
  - Writing and debugging SQL DDL and DML queries to implement and populate a relational database
3. Back-End Engineering:
  - Implementing a data access tier to synchronise a relational database and object-oriented system
  - Creating roles, user privileges and views to regulate access to data
  - Designing SQL injection attacks and thwarting them with stored procedures
  - Implementing SQL transactions from a multi-threaded application, using appropriate isolation levels to ensure atomicity and concurrency
  - Simulating database recovery by hand from a database log
