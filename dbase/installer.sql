-- noinspection SqlNoDataSourceInspectionForFile

/**
Database creation script
*/
/* destroy all tables */
drop table if exists program;
drop table if exists program_coaches;
drop table if exists coach;
drop table if exists member;
drop table if exists comment;
drop table if exists news;
drop table if exists event;

/* enable foreign key constraint */
pragma foreign_keys = on;

create table program(
    program_id integer primary key autoincrement not null,
    name text not null unique,
    subtitle text not null unique,
    content text not null,
    coachingfee real not null,
    boathire real not null,
    image text not null,
    updated_at date
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    content text not null,
    updated_at date
);

create table member(
    member_id integer primary key autoincrement not null,
    first_name text not null,
    second_name text not null,
    email text unique not null,
    password text not null,
    authorisation integer not null
);

create table event(
    event_id integer primary key autoincrement not null,
    title text not null unique,
    content text not null,
    event_date date
);

/* events */
insert into event(title, content, event_date)
values(
       'AON 420 clinic at Evans Bay',
       'Runs over 3 days.',
       '2022-12-18 08:30:00'
       );

insert into event(title, content, event_date)
values(
       'Evans Bay Regatta',
       'Runs over 3 days.',
       '2023-02-18 08:30:00'
       );

insert into event(title, content, event_date)
values(
       '420 Nationals at Naval Point in ChCh',
       'Runs over 2 days.',
       '2023-04-10 08:30:00'
       );



/* members */
insert into member(first_name, second_name, email, password, authorisation)
values(
       'Bri' , 'Monatana', 'bm@gmail.com', 'temp',1
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Darby' , 'Jones', 'dj@gmail.com', 'temp', 1
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Locky' , 'Johanson', 'lj@gmail.com', 'temp',1
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Warren' , 'Perez', 'wp@gmail.com', 'temp',0
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Finn' , 'Reilly', 'fr@gmail.com', 'temp',1
      );

insert into member(first_name, second_name, email, password,authorisation)
values(
       'Helena' , 'Constantine', 'hc@gmail.com', 'temp',1
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Daniel' , 'Liebovitz', 'dl@gmail.com', 'temp',1
      );

insert into member(first_name, second_name, email, password, authorisation)
values(
       'Andy' , 'Twoombly', 'at@gmail.com', 'temp',1
      );


/* News */
insert into news(title, content, updated_at)
values('TRIYA Learn to sail and sailing development starts on the first day T4.',
       'WC has lined up for Mondays, Tuesdays is girls day, Wednesdays is Teams Racing,' ||
       'Thursdays other colleges, Fridays Scots College.' ||
       'However the "allocated" days are not exclusive. We will do our best to make it work for you',
       '2022-08-21 18:45:41'
       );

insert into news(title, content, updated_at)
values('The summer program for Fleet sailing advanced',
       ' The program culminates in an AON sponsored YNZ coaching clinic in Mid December this year.' ||
       'A new program running through to the 420 Nationals will begin in the new year.',
       '2022-09-01 18:00:00'
       );

insert into news(title, content, updated_at)
values('Winter 420 coaching program is under way',
    'We have room for one more person to make up an eve ' ||
    'number for the sailing double handed. College age ' ||
    'students. Competent sailor.ready for trapeze and ' ||
    'spinnaker handling. Wanting to go places',
    '2022-07-30 06:40:00'
       );

insert into news(title, content, updated_at)
values('TRIYA Winter Programme',
    'This programme is designed to develop teams (skipper and crew) ' ||
    'to be able to perform creditably in a National contest. We hope ' ||
    'that you have fun and enjoy yourself and develop your skills ' ||
    'to perform well at that level.',
    '2022-07-30 06:40:00'
       );











/* Programs */


insert into program(name, subtitle, content, coachingfee, boathire,image,updated_at)
values('Learn to Sail',
'This is on weekdays from 4pm until 8pm',
'Focuses on the basics of sailing learning how to tack, gybe, position in the boat and ' ||
'rigging. Currently this runs everyday after school apart from a Wednesday and is ' ||
'perfect for gaining confidence in and around a 420 boat. If your sailor has' ||
'raced another type of boat before or are new to sailing this is the course for them.',
190,
0,
'boats_9.png',
 datetime('now', '-1 months', '+200 minutes' , '-59 seconds')
);

insert into program(name, subtitle, content, coachingfee, boathire,image,updated_at)
values('Teams'' Sailing',
'Short course sailing',
'This is for more experienced sailors who are interested in tactics, teams' ||
'racing consists of 3 boats (2 people per boat) per team and two teams,' ||
'they complete in a short course race(less than 15 minutes long).' ||
'The team that wins is the one that gets the most amount of boats over the line first,' ||
'TRIYA is aiming to have 3 teams compete in the regionals, 1 from Wellington College,' ||
'1 open team and 1 from Scots College.',
170,
0,
'boats_10.png',
 datetime('now', '-4 months', '+200 minutes' , '-59 seconds')
);

insert into program(name, subtitle, content, coachingfee, boathire,image,updated_at)
values('Fleet Racing',
'Trapezing and kiting',
'This is for sailors aiming to compete in Nationals in 2023 who are' ||
'graduates of one of the sailing programs offered, each boats consists of a skipper' ||
'and a crew. The crew will learn how to trapeze and mange a kite, and the skipper will' ||
'be in charge of steering and controls to effect the main sail.' ||
'Fleet racing sails on a Saturday with training in the morning and racing in the afternoon.'
,
300,
125,
'boats_11.png',
 datetime('now', '-4 months', '+200 minutes' , '-59 seconds')
);


























