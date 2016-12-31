/*
GroceryDirect: Database Creation

Author: Melanie Cornelius, mseryn
Written for CS 425-02 Fall 2016 Project
*/

/*
 * Primary Tables
*/

create table persons 
(
    id              integer primary key autoincriment,
    username        varchar(20) not null unique,
    password        varchar(20) not null,
    first_name      varchar(20) not null,
    middle_initial  char(1),
    last_name       varchar(20) not null,
    cart_id         integer foreign key references orders(id),
    type_id         integer foreign key references person_types(id),
    salary          numeric(8, 2),
    job_title       varchar(20),
    balance         numeric(8, 2)
    default_billing_address     integer foreign key references addresses(id),
    default_shipping_address    integer foreign key references addresses(id),
    default_warehouse_address   integer foreign key references addresses(id),
    default_supplier_address    integer foreign key references addresses(id)
)

create table orders
(
    id              integer primary key autoincriment,
    person_id       integer foreign key references persons(id),
    status_id       integer foreign key references order_statuses(id),
    billing_addr_id integer foreign key references addresses(id),
    shipping_addr_id integer foreign key references addresses(id),
    submission_date timestamp,
    total_cost      numeric(8, 2)
)

create table products
(
    id              integer primary key autoincriment,
    product_type_id integer foreign key references product_types(id),
    image_id        integer foreign key references product_images(id),
    price           numeric(8, 2) not null,
    description     varchar(255),
    nutrition_facts varchar(255),
    alcohol_content varchar(255)
)

*create table warehouses
(
    id              integer primary key autoincriment,
    address_id      integer foreign key references addresses(id),
    capacity        integer not null
)

create table addresses
(
    id              integer primary key autoincriment,
    person_id       integer foreign key references persons(id),
    street          varchar(255) not null,
    apartment_no    varchar(255),
    city            varchar(255) not null,
    state_code_id   integer foreign key references state_codes(id),
    zip_code        numeric(5, 0) not null,
    address_type    integer foreign key references address_types(id)
)

create table credit_cards
(
    id              integer primary key autoincriment,
    person_id       integer foreign key references persons(id),
    card_number     numeric(16, 0) not null,
    expiration_date date not null,
    security_code   numeric(3, 0) not null,
    card_type_id    integer foreign key references card_types(id),
    billing_address_id integer foreign key references addresses(id)
)

create table product_images
(
    id              integer primary key autoincriment,
    image_type      varchar(5) not null,
    image_data      blob not null
)

/*
 * Enumeration Tables
*/

create table person_types
(
    id              integer primary key autoincriment,
    person_type     varchar(50) not null 
)

create table product_types
(
    id              integer primary key autoincriment,
    product_type    varchar(50) not null 
)

create table address_types
(
    id              integer primary key autoincriment,
    address_type    varchar(50) not null 
)

create table order_status
(
    id              integer primary key autoincriment,
    order_status    varchar(50) not null 
)

create table state_codes
(
    /* Note: table exists for ease of code verification */
    id              integer primary key autoincriment,
    state_code      char(2) not null 
)

/*
 * Link Tables
*/

create table order_to_product
(
    order_id        integer foreign key references orders(id),
    product_id      integer foreign key references products(id)
)

create tabe warehouse_to_product
(
    warehouse_id    integer foreign key references warehouses(id),
    product_id      integer foreign key references products(id)
)

/*
 * Constructing Enum Tables
*/

TODO
