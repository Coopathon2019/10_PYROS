CREATE TABLE Ingredients (
    Ingredient text NOT NULL,
    Calories float,
    Price float NOT NULL,
    Gram float,
    UnknownPrice Boolean,
    PRIMARY KEY (Ingredient)
);
CREATE TABLE Dishes (
    Dishname text NOT NULL,
    Calories float,
    Persons float,
    Difficulty float,
    PRIMARY KEY (Dishname)
);
CREATE TABLE Record (
    Userid text,
    RecordDate DATE DEFAULT CURRENT_DATE,
    Dish text,
    Calories float,
    image bytea,
    Count int
);
CREATE TABLE Liked (
    Userid text,
    Dishname text
);
CREATE TABLE LastMsg (
    Userid text,
    msg text,
    msgTime TIMESTAMP DEFAULT NOW()
);
CREATE TABLE Cart (
    Userid text,
    Dish text,
    Ingredients text[]
);