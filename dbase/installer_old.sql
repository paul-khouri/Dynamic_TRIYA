-- noinspection SqlNoDataSourceInspectionForFile

/**
Database creation script
*/
/* destroy all tables */
drop table if exists page;
drop table if exists newsitem;
drop table if exists coach;
drop table if exists program;
drop table if exists member;

/* enable foreign key constraint */
pragma foreign_keys = on;

create table page(
    id integer primary key autoincrement not null,
    header text not null,
    content text not null,
    image text not null,
    pagenumber integer not null,
    updated_at date
);

create table newsitem(
    id integer primary key autoincrement not null,
    header text not null,
    details text not null,
    content text not null,
    updated_at date
);


create table member(
    id integer primary key autoincrement not null,
    firstname text not null,
    secondname text not null,
    phone text not null,
    email text not null,
    streetaddress text not null,
    suburb text not null,
    updated_at date,
    username text unique not null,
    password text not null,
    authorisation integer not null
);

create table coach(
    id integer not null unique,
    bio text not null,
    updated_at date,
    foreign key (id) references member(id)
);

create table program(
    id integer primary key autoincrement not null,
    name text not null,
    subtitle text not null,
    description text not null,
    coachingfee real not null,
    boathire real not null,
    image text not null,
    updated_at date
);

/* Pages */
insert into page(header, content, image, pagenumber, updated_at)
values('Who are we?',
'TRIYAs aim is to make sailing accessible to all ' ||
'school age students to encourage a love for the water ' ||
'and sailing.We run programs from beginner levels all the ' ||
'way to national champions.',
'roll_no_wind.jpg',
1,
date('now')
);

insert into page(header, content, image, pagenumber, updated_at)
values('420 Sailing',
'TRIYAs aim is to make sailing accessible to all school age students to encourage a love for'||
'the water and sailing. We run programs from beginner levels all the way to national champions.',
'inboat_upwind.jpg',
1,
date('now')
);

/* News Item */
insert into newsitem(header, details, content, updated_at)
values('Kids Sailing Day',
'Running Saturday 21 November, 9am to 3pm, Cost=$25.00',
'For children an introductory sailing day. No need to register.
Come down.
Children must have a parent or guardian with them',
datetime('now')
);

/* Programs */
insert into program(name, subtitle, description, coachingfee, boathire,image,updated_at)
values('Learn to Sail',
'This is on weekdays from 4pm until 8pm',
'Focuses on the basics of sailing learning how to tack, gybe, position in the boat and ' ||
'rigging. Currently this runs everyday after school apart from a Wednesday and is ' ||
'perfect for gaining confidence in and around a 420 boat. If your sailor has' ||
'raced another type of boat before or are new to sailing this is the course for them.',
190,
0,
'set_up_opt.jpg',
date('now')
);


insert into program(name, subtitle, description, coachingfee, boathire,image,updated_at)
values(
'Teams Racing',
'Short course sailing',
'This is for more experienced sailors who are interested in tactics, teams
racing consists of 3 boats (2 people per boat) per team and two teams,
they complete in a short course race(less than 15 minutes long).
The team that wins is the one that gets the most amount of boats over the line first,
TRIYA is aiming to have 3 teams compete in the regionals, 1 from
Wellington College, 1 open team and 1 from Scots College.',
170,
0,
'ramp_late.jpg',
date('now')
);

insert into program(name, subtitle, description, coachingfee, boathire,image,updated_at)
values(
'Fleet Racing',
'Trapezing and Kiting',
'This is for sailors aiming to compete in Nationals in 2023 who are graduates
of one of the sailing programs offered, each boats consists of a skipper and a crew.
The crew will learn how to trapeze and mange a kite, and the skipper will be in charge
of steering and controls to effect the main sail. Fleet racing sails on a Saturday with
training in the morning and racing in the afternoon.',
300,
125,
'fleet_racing.jpg',
date('now')
);

/* member */
insert into member(firstname,secondname,phone,email,streetaddress,suburb,updated_at,username,password,authorisation)
values('Warren', 'Smith', '021236673', 'waz@gmail.com', '67 Noodle Lane', 'Karori',datetime('now'), 'admin', 'temp', 0);



























