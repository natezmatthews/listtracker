drop table if exists risuto;
create table risuto (
  risuto_id integer primary key autoincrement,
  text text not null,
  name text not null,
  description text,
  created integer
);