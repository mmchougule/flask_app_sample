drop table if exists user;
create table employee (
  employee_id integer primary key autoincrement,
  firstname text not null,
  lastname text not null,
  company_id integer not null,
  email text not null
);

create table company (
  company_id integer primary key autoincrement,
  company_name text not null,
  address text not null,
  revenue text not null
);
