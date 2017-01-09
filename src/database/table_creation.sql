/*
 * GroceryDirect: Database Creation
 *
 * Author: Melanie Cornelius, mseryn
 * Written for CS 425-02 Fall 2016 Project
*/

drop table state_code_to_product ;
drop table supplier_to_product ;
drop table warehouse_to_product ;
drop table order_to_product ;

drop table persons ;
drop table warehouses ;
drop table orders ;
drop table products ;
drop table product_images ;
drop table credit_cards ;
drop table addresses ;

drop table card_types ;
drop table state_codes ;
drop table order_statuses ;
drop table address_types ;
drop table product_types ;
drop table person_types ;


/*
 * Enumeration Tables
*/

CREATE TABLE person_types
(
    id              integer generated always as identity primary key,
    person_type     varchar(50) not null
);

create table product_types
(
    id              integer generated always as identity primary key,
    product_type    varchar(50) not null 
);

create table address_types
(
    id              integer generated always as identity primary key,
    address_type    varchar(50) not null 
);

create table order_statuses
(
    id              integer generated always as identity primary key,
    order_status    varchar(50) not null 
);

create table state_codes
(
    /* Note: table exists for ease of code verification */
    id              integer generated always as identity primary key,
    state_code      char(2) not null 
);

create table card_types
(
    id              integer generated always as identity primary key,
    card_type       varchar(20) not null
);


/*
 * Primary Tables
*/


create table addresses
(
    id              integer generated always as identity primary key,
    street          varchar(255) not null,
    apartment_no    varchar(255),
    city            varchar(255) not null,
    zip_code        integer not null,
    state_code_id   integer not null,
    address_type    integer not null,
    constraint      state_code_fk   foreign key (state_code_id) references state_codes(id),
    constraint      address_type_fk foreign key (address_type)  references address_types(id)
);


create table orders
(
    id              integer generated always as identity primary key,
    submission_date timestamp,
    total_cost      numeric(8, 2),
    status_id       integer,
    billing_addr_id integer,
    shipping_addr_id integer,
    constraint      status_fk              foreign key (status_id)        references order_statuses(id),
    constraint      order_billing_addr_fk  foreign key (billing_addr_id)  references addresses(id),
    constraint      order_shipping_addr_fk foreign key (shipping_addr_id) references addresses(id)
);

create table credit_cards
(
    id              integer generated always as identity primary key,
    card_number     numeric(16, 0) not null,
    security_code   numeric(3, 0) not null,
    expiration_date date not null,
    /*
    person_id       integer,
    */
    card_type_id    integer,
    billing_addr_id integer,
    /*
    person_id       integer foreign key (person_id) references persons(id),
    */
    constraint      card_type_fk         foreign key (card_type_id)    references card_types(id),
    constraint      card_billing_addr_fk foreign key (billing_addr_id) references addresses(id)
);



create table persons 
(
    id              integer generated always as identity primary key,
    username        varchar(20) not null unique,
    password        varchar(20) not null,
    first_name      varchar(20) not null,
    middle_initial  char(1),
    last_name       varchar(20) not null,
    salary          numeric(8, 2),
    job_title       varchar(20),
    balance         numeric(8, 2),
    cart_id         integer,
    person_type_id  integer,
    default_billing_address     integer,
    default_shipping_address    integer,
    default_warehouse_address   integer,
    default_supplier_address    integer,
    constraint      cart_fk        foreign key (cart_id)        references orders(id),
    constraint      person_type_fk foreign key (person_type_id) references person_types(id),
    constraint      default_billing_addr_fk    foreign key (default_billing_address)   references addresses(id),
    constraint      default_shipping_addr_fk   foreign key (default_shipping_address)  references addresses(id),
    constraint      default_warehouse_addr_fk  foreign key (default_warehouse_address) references addresses(id),
    constraint      default_supplier_addr_fk   foreign key (default_supplier_address)  references addresses(id)
);

create table product_images
(
    id              integer generated always as identity primary key,
    image_type      varchar(5) not null,
    image_data      blob not null
);

create table products
(
    id              integer generated always as identity primary key,
    name            varchar(20) not null,
    description     varchar(255),
    nutrition_facts varchar(255),
    alcohol_content varchar(255),
    product_type_id integer,
    image_id        integer,
    constraint      product_type_fk foreign key (product_type_id) references product_types(id),
    constraint      image_fk        foreign key (image_id)        references product_images(id)
);

create table warehouses
(
    id              integer generated always as identity primary key,
    capacity        integer not null,
    address_id      integer,
    constraint      address_fk foreign key (address_id) references addresses(id)
);


/*
 * Link Tables
*/

create table order_to_product
(
    order_id        integer,
    product_id      integer,
    order_price     numeric(8, 2) not null,
    constraint order_to_product_fk foreign key (order_id)   references orders(id),
    constraint product_to_order_fk foreign key (product_id) references products(id)
);

create table warehouse_to_product
(
    warehouse_id    integer,
    product_id      integer,
    constraint warehouse_to_product_fk foreign key (warehouse_id) references warehouses(id),
    constraint product_to_warehouse_fk foreign key (product_id)   references products(id)
);

create table state_code_to_product
(
    state_id        integer,
    product_id      integer,
    state_price     numeric(8, 2) not null,
    constraint state_code_to_product_fk  foreign key (state_id)   references state_codes(id),
    constraint product_to_state_fk  foreign key (product_id) references products(id)
);

create table supplier_to_product
(
    supplier_id     integer,
    product_id      integer,
    supplier_price  numeric(8, 2) not null,
    constraint supplier_to_product_fk foreign key (supplier_id) references persons(id),
    constraint product_to_supplier_fk foreign key (product_id)  references products(id)
);

select * from DUAL;


/*TODO*/
