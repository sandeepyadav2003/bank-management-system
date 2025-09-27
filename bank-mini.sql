use sandeep;
#################------->user_table<------------

create table bank_user(name varchar(40) NOT NULL,Account_no int NOT NULL,Account_type varchar(30) NOT NULL,amt float Default 0,pin int NOT NULL);
alter table bank_user add constraint primary key(Account_no);
alter table bank_user add strt_date date;
select*from bank_user;
################--------->admin_Table<-----------

create table bank_admin(name varchar(30)Not null,password varchar(20));
select*from bank_admin;
insert into bank_admin values("sandeep","jack");
################--------->transcation_table<-----------

create table bank_Transaction(txt_no int not null,Account_no int not null,txt_type varchar(30) not null,txt_date DATETIME default current_timestamp);
alter table bank_transaction add constraint fk_key foreign key(Account_no) references bank_user(Account_no);
select*from bank_Transaction;
desc bank_transaction;
desc bank_user;