create table if not exists test_sql_b4
(id int auto_increment,
name varchar(255),
primary key(id)
);
insert into test_sql_b4(name) values('Before');
commit;
select * from test_sql_b4;