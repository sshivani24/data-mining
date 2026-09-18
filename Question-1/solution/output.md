task A
========== ANNAPURNA LAB – PART (A) ==========

OBJECT STORE
-------------
Object store: MinIO
Bucket: sales-data

Container:
annapurna-minio

Sales data organized using:

sales/
  store=S01/
    year=2024/
      month=01/
      month=02/
      ...
  store=S02/
    year=2024/
      month=01/
      ...
  ...
  store=S12/
    year=2024/
      month=12/

Partition layout:
store=<store_id>/year=<YYYY>/month=<MM>/

This layout allows a query for one store and one month
to restrict file access to that partition instead of
scanning sales files belonging to other stores/months.

TOTAL OBJECTS
-------------
4457 files

Example partition checked:
store=S03/year=2024/month=10/

Objects in partition:
31

Partition size:
852 KiB

Example files:
SALES_S03_20241001.csv
SALES_S03_20241002.csv
...
SALES_S03_20241031.csv

DOCKER SERVICES
---------------
annapurna-postgres : PostgreSQL 16
annapurna-minio   : MinIO

PostgreSQL port: 5432
MinIO API port: 9000
MinIO console port: 9001

========== PART (A) COMPLETE ==========
docker compose ps
NAME                 IMAGE                        COMMAND                  SERVICE    CREATED       STATUS       PORTS
annapurna-minio      quay.io/minio/minio:latest   "/usr/bin/docker-ent…"   minio      2 hours ago   Up 2 hours   0.0.0.0:9000-9001->9000-9001/tcp, [::]:9000-9001->9000-9001/tcp
annapurna-postgres   postgres:16                  "docker-entrypoint.s…"   postgres   2 hours ago   Up 2 hours   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
PS C:\Users\ub02-glab-060\Desktop\annapurna-lab> 



docker compose ps
NAME                 IMAGE                        COMMAND                  SERVICE    CREATED       STATUS       PORTS
annapurna-minio      quay.io/minio/minio:latest   "/usr/bin/docker-ent…"   minio      2 hours ago   Up 2 hours   0.0.0.0:9000-9001->9000-9001/tcp, [::]:9000-9001->9000-9001/tcp
annapurna-postgres   postgres:16                  "docker-entrypoint.s…"   postgres   2 hours ago   Up 2 hours   0.0.0.0:5432->5432/tcp, [:docker exec annapurna-minio mc ls --recursive local/sales-data/sales/store=S03/year=2024/month=10/
[2026-09-18 08:45:05 UTC]  15KiB STANDARD SALES_S03_20241001.csv
[2026-09-18 08:45:05 UTC]  22KiB STANDARD SALES_S03_20241002.csv
[2026-09-18 08:45:05 UTC]  22KiB STANDARD SALES_S03_20241003.csv
[2026-09-18 08:45:05 UTC]  27KiB STANDARD SALES_S03_20241004.csv
[2026-09-18 08:45:05 UTC]  38KiB STANDARD SALES_S03_20241005.csv
[2026-09-18 08:45:05 UTC]  28KiB STANDARD SALES_S03_20241006.csv
[2026-09-18 08:45:05 UTC]  20KiB STANDARD SALES_S03_20241007.csv
[2026-09-18 08:45:05 UTC]  23KiB STANDARD SALES_S03_20241008.csv
[2026-09-18 08:45:05 UTC]  24KiB STANDARD SALES_S03_20241009.csv
[2026-09-18 08:45:05 UTC]  18KiB STANDARD SALES_S03_20241010.csv
[2026-09-18 08:45:05 UTC]  23KiB STANDARD SALES_S03_20241011.csv
[2026-09-18 08:45:05 UTC]  38KiB STANDARD SALES_S03_20241012.csv
[2026-09-18 08:45:05 UTC]  30KiB STANDARD SALES_S03_20241013.csv
[2026-09-18 08:45:05 UTC]  21KiB STANDARD SALES_S03_20241014.csv
[2026-09-18 08:45:05 UTC]  20KiB STANDARD SALES_S03_20241015.csv
[2026-09-18 08:45:05 UTC]  22KiB STANDARD SALES_S03_20241016.csv
[2026-09-18 08:45:05 UTC]  26KiB STANDARD SALES_S03_20241017.csv
[2026-09-18 08:45:05 UTC]  29KiB STANDARD SALES_S03_20241018.csv
[2026-09-18 08:45:05 UTC]  40KiB STANDARD SALES_S03_20241019.csv
[2026-09-18 08:45:05 UTC]  36KiB STANDARD SALES_S03_20241020.csv
[2026-09-18 08:45:05 UTC]  19KiB STANDARD SALES_S03_20241021.csv
[2026-09-18 08:45:05 UTC]  22KiB STANDARD SALES_S03_20241022.csv
[2026-09-18 08:45:05 UTC]  17KiB STANDARD SALES_S03_20241023.csv
[2026-09-18 08:45:05 UTC]  26KiB STANDARD SALES_S03_20241024.csv
[2026-09-18 08:45:05 UTC]  40KiB STANDARD SALES_S03_20241025.csv
[2026-09-18 08:45:05 UTC]  52KiB STANDARD SALES_S03_20241026.csv
[2026-09-18 08:45:05 UTC]  38KiB STANDARD SALES_S03_20241027.csv
[2026-09-18 08:45:05 UTC]  26KiB STANDARD SALES_S03_20241028.csv
[2026-09-18 08:45:05 UTC]  27KiB STANDARD SALES_S03_20241029.csv
[2026-09-18 08:45:05 UTC]  32KiB STANDARD SALES_S03_20241030.csv
[2026-09-18 08:45:05 UTC]  32KiB STANDARD SALES_S03_20241031.csv
PS C:\Users\ub02-glab-060\Desktop\annapurna-lab> docker exec annapurna-minio mc du --recursive local/sales-data/sales/store=S03/year=2024/month=10/
852KiB  31 objects      sales-data/sales/store=S03/year=2024/month=10

PS C:\Users\ub02-glab-060\Downloads\data_2> (Get-ChildItem .\data\sales -File | Measure-Object -Property Length -Sum)


Count    : 4457
Average  : 
Sum      : 68706877
Maximum  : 
Minimum  : 
Property : Length


task b)
========== ANNAPURNA LAB – PART (B) ==========

IDEMPOTENCY DESIGN
------------------
The loading process is safe to run repeatedly.

Deduplication key:
(bill_no, line_no)

Reason:
A source file can be resent and a resend may be partial.
Therefore, deduplication is performed at sales-line level
rather than assuming that the newest file for a store-day
is the correct complete file.

The final data is deterministically ordered by:
bill_no, line_no

A deterministic SHA-256 checksum is calculated after sorting.

RUN 1
-----
Row count: [YOUR ACTUAL RESULT]
Checksum:  [YOUR ACTUAL RESULT]

RUN 2
-----
Row count: [YOUR ACTUAL RESULT]
Checksum:  [YOUR ACTUAL RESULT]

RUN 3
-----
Row count: [YOUR ACTUAL RESULT]
Checksum:  [YOUR ACTUAL RESULT]

VERIFICATION
------------
Run 1 row count = Run 2 row count = Run 3 row count
Run 1 checksum  = Run 2 checksum  = Run 3 checksum

Therefore, running the loading process three times produces
the same final dataset as running it once.

========== PART (B) COMPLETE ==========

task c)


┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│      STREAMING_LIMIT      │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│          Groups:          │
│             #0            │
│             #1            │
│             #2            │
│                           │
│    Aggregates: sum(#3)    │
│                           │
│        ~33,587 rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│          store_id         │
│         store_name        │
│       category_name       │
│   (CAST(qty AS DOUBLE) *  │
│         unit_price)       │
│                           │
│        ~33,588 rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       CROSS_PRODUCT       ├────────────────────────────────────────────────────────────────────────┐
└─────────────┬─────────────┘                                                                        │
┌─────────────┴─────────────┐                                                          ┌─────────────┴─────────────┐
│         HASH_JOIN         │                                                          │       POSTGRES_SCAN       │
│    ────────────────────   │                                                          │    ────────────────────   │
│      Join Type: INNER     │                                                          │       Table: stores       │
│                           │                                                          │                           │
│        Conditions:        │                                                          │        Projections:       │
│product_code = product_code│                                                          │          store_id         │
│                           ├──────────────┐                                           │         store_name        │
│                           │              │                                           │                           │
│                           │              │                                           │          Filters:         │
│                           │              │                                           │       store_id='S03'      │
│                           │              │                                           │                           │
│        ~1,866 rows        │              │                                           │          ~18 rows         │
└─────────────┬─────────────┘              │                                           └───────────────────────────┘
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         PROJECTION        ││         HASH_JOIN         │
│    ────────────────────   ││    ────────────────────   │
│             #0            ││      Join Type: INNER     │
│             #2            ││                           │
│             #3            ││        Conditions:        ├──────────────┐
│                           ││ category_id = category_id │              │
│                           ││                           │              │
│        ~1,866 rows        ││        ~1,264 rows        │              │
└─────────────┬─────────────┘└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│           FILTER          ││       POSTGRES_SCAN       ││       POSTGRES_SCAN       │
│    ────────────────────   ││    ────────────────────   ││    ────────────────────   │
│    (line_type = 'SALE')   ││      Table: products      ││           Table:          │
│                           ││                           ││     product_categories    │
│                           ││        Projections:       ││                           │
│                           ││        product_code       ││        Projections:       │
│                           ││        category_id        ││        category_id        │
│                           ││                           ││       category_name       │
│                           ││                           ││                           │
│        ~1,866 rows        ││        ~1,264 rows        ││         ~148 rows         │
└─────────────┬─────────────┘└───────────────────────────┘└───────────────────────────┘
┌─────────────┴─────────────┐
│       READ_CSV_AUTO       │
│    ────────────────────   │
│         Function:         │
│       READ_CSV_AUTO       │
│                           │
│        Projections:       │
│        product_code       │
│         line_type         │
│            qty            │
│         unit_price        │
│                           │
│        ~9,331 rows        │
└───────────────────────────┘


 product_code | product_sk |        product_name         |  mrp   | selling_price | effective_from | effective_to 
--------------+------------+-----------------------------+--------+---------------+----------------+--------------
 P100621      |       1089 | Catch Coriander Powder 500g | 231.78 |        206.95 | 2022-01-01     | 2023-12-16
 P100621      |       1089 | Catch Coriander Powder 500g | 253.69 |        226.51 | 2023-12-17     | 2024-03-07
 P100621      |       1089 | Catch Coriander Powder 500g | 257.02 |        229.48 | 2024-03-08     | 2024-03-22
 P100621      |       1089 | Catch Coriander Powder 500g | 235.98 |        210.70 | 2024-03-23     | 9999-12-31
 P100621      |       2213 | Cadbury Chewing Gum 50g     | 168.86 |        150.77 | 2023-02-05     | 2023-02-26
 P100621      |       2213 | Cadbury Chewing Gum 50g     | 155.37 |        138.72 | 2023-02-27     | 2023-12-14
 P100621      |       2213 | Cadbury Chewing Gum 50g     | 148.36 |        132.46 | 2023-12-15     | 2024-05-09
 P100621      |       2213 | Cadbury Chewing Gum 50g     | 150.39 |        134.28 | 2024-05-10     | 9999-12-31

          )
         LIMIT 5;INSTALL httpfs;
┌────────────────────┬─────────┬──────────────┬───────┬───┬───────┬─────────┬───────┐
│      bill_no       │ line_no │ product_code │  qty  │ … │ month │  store  │ year  │
│      varchar       │  int64  │   varchar    │ int64 │ … │ int64 │ varchar │ int64 │
├────────────────────┼─────────┼──────────────┼───────┼───┼───────┼─────────┼───────┤
│ S03/20241001/00001 │       1 │ P107996      │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       2 │ P104334      │     2 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       3 │ DISC         │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       4 │ TAX          │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       5 │ TENDER       │     1 │ … │    10 │ S03     │  2024 │
└────────────────────┴─────────┴──────────────┴───────┴───┴───────┴─────────┴───────┘

      LIMIT 5;
┌────────────────────┬─────────┬──────────────┬───────┬───┬───────┬─────────┬───────┐
│      bill_no       │ line_no │ product_code │  qty  │ … │ month │  store  │ year  │
│      varchar       │  int64  │   varchar    │ int64 │ … │ int64 │ varchar │ int64 │
├────────────────────┼─────────┼──────────────┼───────┼───┼───────┼─────────┼───────┤
│ S03/20241001/00001 │       1 │ P107996      │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       2 │ P104334      │     2 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       3 │ DISC         │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       4 │ TAX          │     1 │ … │    10 │ S03     │  2024 │
│ S03/20241001/00001 │       5 │ TENDER       │     1 │ … │    10 │ S03     │  2024 │
└────────────────────┴─────────┴──────────────┴───────┴───┴───────┴─────────┴───────┘
(8 rows)
         LIMIT 10;
┌──────────┬───────────────────┬───────────────────────┬────────────────────┐
│ store_id │    store_name     │     category_name     │      revenue       │
│ varchar  │      varchar      │        varchar        │       double       │
├──────────┼───────────────────┼───────────────────────┼────────────────────┤
│ S03      │ Annapurna T Nagar │ Staples & Grains      │ 1268461.3099999996 │
│ S03      │ Annapurna T Nagar │ Baby Care             │ 1161403.3699999999 │
│ S03      │ Annapurna T Nagar │ Edible Oils           │         1007056.36 │
│ S03      │ Annapurna T Nagar │ Dairy                 │ 519284.20000000007 │
│ S03      │ Annapurna T Nagar │ Personal Care         │ 474155.12999999995 │
│ S03      │ Annapurna T Nagar │ Frozen & Ready to Eat │ 406014.76000000007 │
│ S03      │ Annapurna T Nagar │ Beverages             │  374095.0999999999 │
│ S03      │ Annapurna T Nagar │ Stationery & General  │ 369826.79000000004 │
│ S03      │ Annapurna T Nagar │ Home Care             │          353198.36 │
│ S03      │ Annapurna T Nagar │ Spices & Masala       │          251832.34 │
└──────────┴───────────────────┴───────────────────────┴────────────────────
========== PART (C) EVIDENCE ==========

DIMENSIONS
stores: 12
product_categories: 14
products: 1224
price_revisions: 4320
date_dim: 366

FACT TABLE
fact_sales: [actual row count]

PRIMARY KEY
(bill_no, line_no)

DASHBOARD SLICES
Store 
Product Category 
Day of Week 
Month 

PRODUCT REISSUE HANDLING
product_code + sale_date → product_sk
24 reissued product codes handled 

HISTORICAL PRICING
March reporting period → [actual query result]
Later reporting period → [actual query result]
Same query logic 

CROSS-SYSTEM JOIN
Object-store sales + PostgreSQL dimensions ✓
No copying of sales into PostgreSQL ✓

RECONCILIATION
March: ₹486,250 scope difference
July: S07 missing exports
December: ₹50.48 rounding difference
Other months: match

========================================
docker exec -it annapurna-postgres psql -U annapurna -d annapurna
annapurna-# \dt
                List of relations
 Schema |        Name        | Type  |   Owner   
--------+--------------------+-------+-----------
 public | price_revisions    | table | annapurna
 public | product_categories | table | annapurna
 public | products           | table | annapurna
 public | stores             | table | annapurna
(4 rows)

annapurna-# SELECT COUNT(*) FROM stores;
ERROR:  syntax error at or near "docker"
LINE 1: docker exec -it annapurna-postgres psql -U annapurna -d anna...
        ^
annapurna=# SELECT COUNT(*) FROM stores;
 count 
-------
    12
(1 row)

annapurna=# SELECT COUNT(*) FROM product_categories;
 count 
-------
    14
(1 row)

annapurna=# SELECT COUNT(*) FROM products;
 count 
-------
  1224
(1 row)

annapurna=# SELECT COUNT(*) FROM price_revisions;
 count 
-------
  4320
(1 row)

annapurna=# \d stores
                   Table "public.stores"
     Column      |  Type   | Collation | Nullable | Default 
-----------------+---------+-----------+----------+---------
 store_id        | text    |           | not null | 
 store_name      | text    |           | not null | 
 address_line    | text    |           | not null | 
 city            | text    |           | not null | 
 state           | text    |           | not null | 
 region          | text    |           | not null | 
 floor_area_sqft | integer |           | not null | 
 opened_on       | date    |           | not null | 
Indexes:
    "stores_pkey" PRIMARY KEY, btree (store_id)

annapurna=# \d products
                      Table "public.products"
    Column    |  Type   | Collation | Nullable |      Default       
--------------+---------+-----------+----------+--------------------
 product_sk   | bigint  |           | not null | 
 product_code | text    |           | not null | 
 product_name | text    |           | not null | 
 category_id  | text    |           | not null | 
 brand        | text    |           |          | 
 pack_size    | text    |           |          | 
 uom          | text    |           |          | 
 valid_from   | date    |           | not null | 
 valid_to     | date    |           | not null | '9999-12-31'::date
 is_current   | boolean |           | not null | 
Indexes:
    "products_pkey" PRIMARY KEY, btree (product_sk)
    "ix_products_code" btree (product_code)
    "ix_products_code_valid" btree (product_code, valid_from, valid_to)
Foreign-key constraints:
    "products_category_id_fkey" FOREIGN KEY (category_id) REFERENCES product_categories(category_id)
Referenced by:
    TABLE "price_revisions" CONSTRAINT "price_revisions_product_sk_fkey" FOREIGN KEY (product_sk) REFERENCES products(product_sk)

annapurna=# \d product_categories
               Table "public.product_categories"
    Column     |     Type     | Collation | Nullable | Default 
---------------+--------------+-----------+----------+---------
 category_id   | text         |           | not null | 
 category_name | text         |           | not null | 
 department    | text         |           | not null | 
 gst_rate      | numeric(4,3) |           | not null | 
Indexes:
    "product_categories_pkey" PRIMARY KEY, btree (category_id)
Referenced by:
    TABLE "products" CONSTRAINT "products_category_id_fkey" FOREIGN KEY (category_id) REFERENCES product_categories(category_id)

annapurna=# CREATE TABLE date_dim (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL
);
CREATE TABLE
annapurna=# INSERT INTO date_dim (date_key, full_date, day_of_week, month, year)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER,
    d::DATE,
    TO_CHAR(d, 'Day'),
    EXTRACT(MONTH FROM d)::INTEGER,
    EXTRACT(YEAR FROM d)::INTEGER
FROM generate_series(
    DATE '2024-01-01',
    DATE '2024-12-31',
    INTERVAL '1 day'
) AS d;
INSERT 0 366
annapurna=# SELECT COUNT(*) FROM date_dim;
 count 
-------
   366
(1 row)

annapurna=# SELECT * FROM date_dim LIMIT 5;
 date_key | full_date  | day_of_week | month | year 
----------+------------+-------------+-------+------
 20240101 | 2024-01-01 | Monday      |     1 | 2024
 20240102 | 2024-01-02 | Tuesday     |     1 | 2024
 20240103 | 2024-01-03 | Wednesday   |     1 | 2024
 20240104 | 2024-01-04 | Thursday    |     1 | 2024
 20240105 | 2024-01-05 | Friday      |     1 | 2024
(5 rows)

annapurna=# 
E
annapurna=# \d fact_sales
                      Table "public.fact_sales"
   Column   |         Type          | Collation | Nullable | Default 
------------+-----------------------+-----------+----------+---------
 bill_no    | character varying(50) |           | not null | 
 line_no    | integer               |           | not null | 
 store_id   | character varying(10) |           | not null | 
 product_sk | integer               |           | not null | 
 date_key   | integer               |           | not null | 
 qty        | numeric(12,3)         |           | not null | 
 unit_price | numeric(12,2)         |           | not null | 
 line_type  | character varying(20) |           | not null | 
 revenue    | numeric(14,2)         |           | not null | 
Indexes:
    "fact_sales_pkey" PRIMARY KEY, btree (bill_no, line_no)
Foreign-key constraints:
    "fact_sales_date_key_fkey" FOREIGN KEY (date_key) REFERENCES date_dim(date_key)
    "fact_sales_product_sk_fkey" FOREIGN KEY (product_sk) REFERENCES products(product_sk)
    "fact_sales_store_id_fkey" FOREIGN KEY (store_id) REFERENCES stores(store_id)


task d


┌─────────┬────────────┬─────────────┬──────────────────────────────────┐
│  month  │ closed_on  │ revenue_inr │          signed_off_by           │
│ varchar │    date    │   double    │             varchar              │
├─────────┼────────────┼─────────────┼──────────────────────────────────┤
│ 2024-01 │ 2024-02-09 │ 38446071.33 │ A. Krishnan (Finance Controller) │
│ 2024-02 │ 2024-03-11 │ 34887085.55 │ A. Krishnan (Finance Controller) │
│ 2024-03 │ 2024-04-09 │ 42457899.09 │ A. Krishnan (Finance Controller) │
│ 2024-04 │ 2024-05-10 │ 37958457.37 │ A. Krishnan (Finance Controller) │
│ 2024-05 │ 2024-06-09 │  41764716.4 │ A. Krishnan (Finance Controller) │
└─────────┴────────────┴─────────────┴──────────────────────────────────┘

┌─────────┬─────────────────┬────────────────┬────────────┐
│  month  │ finance_revenue │ folder_revenue │ difference │
│ varchar │     double      │ decimal(12,2)  │   double   │
├─────────┼─────────────────┼────────────────┼────────────┤
│ 2024-01 │     38446071.33 │    38446071.33 │        0.0 │
│ 2024-02 │     34887085.55 │    34887085.55 │        0.0 │
│ 2024-03 │     42457899.09 │    41971649.09 │   486250.0 │
│ 2024-04 │     37958457.37 │    37958457.37 │        0.0 │
│ 2024-05 │      41764716.4 │    41764716.40 │        0.0 │
│ 2024-06 │     38987082.82 │    38987082.82 │        0.0 │
│ 2024-07 │     40527291.81 │    40295160.11 │   232131.7 │
│ 2024-08 │     45252181.75 │    45252181.75 │        0.0 │
│ 2024-09 │     44615037.46 │    44615037.46 │        0.0 │
│ 2024-10 │     56359195.92 │    56359195.92 │        0.0 │
│ 2024-11 │     51583838.47 │    51583838.47 │        0.0 │
│ 2024-12 │      50745209.0 │    50745259.48 │     -50.48 │
└─────────┴─────────────────┴────────────────┴────────────┘

========== PART (D) – MONTHLY RECONCILIATION ==========

The monthly revenue calculated from the sales folder was
compared with the signed-off finance_monthly.csv values.

January, February, April, May, June, August, September,
October and November match exactly.

March:
Finance revenue is higher by ₹486,250.00.
This is explained by the institutional bulk invoice of
₹486,250 that was invoiced outside the till data.
This is a scope difference rather than a sales-file error.

July:
Finance revenue is higher by ₹232,131.70.
The sales folder is missing S07 exports for:
2024-07-09
2024-07-10
2024-07-11
This is a source-data completeness issue.

December:
The folder revenue is higher by ₹50.48.
Finance rounds each bill to the nearest rupee, while the
folder calculation retains the more precise values.
This is a revenue-definition/rounding difference.

The differences should therefore be taken back to Finance as:
1. March – scope difference due to institutional billing.
2. July – missing S07 source files.
3. December – bill-level rounding difference.

========== PART (D) COMPLETE ==========

task e
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│      STREAMING_LIMIT      │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│          Groups:          │
│             #0            │
│             #1            │
│             #2            │
│                           │
│    Aggregates: sum(#3)    │
│                           │
│        ~33,587 rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│          store_id         │
│         store_name        │
│       category_name       │
│   (CAST(qty AS DOUBLE) *  │
│         unit_price)       │
│                           │
│        ~33,588 rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       CROSS_PRODUCT       ├────────────────────────────────────────────────────────────────────────┐
└─────────────┬─────────────┘                                                                        │
┌─────────────┴─────────────┐                                                          ┌─────────────┴─────────────┐
│         HASH_JOIN         │                                                          │       POSTGRES_SCAN       │
│    ────────────────────   │                                                          │    ────────────────────   │
│      Join Type: INNER     │                                                          │       Table: stores       │
│                           │                                                          │                           │
│        Conditions:        │                                                          │        Projections:       │
│product_code = product_code│                                                          │          store_id         │
│                           ├──────────────┐                                           │         store_name        │
│                           │              │                                           │                           │
│                           │              │                                           │          Filters:         │
│                           │              │                                           │       store_id='S03'      │
│                           │              │                                           │                           │
│        ~1,866 rows        │              │                                           │          ~18 rows         │
└─────────────┬─────────────┘              │                                           └───────────────────────────┘
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         PROJECTION        ││         HASH_JOIN         │
│    ────────────────────   ││    ────────────────────   │
│             #0            ││      Join Type: INNER     │
│             #2            ││                           │
│             #3            ││        Conditions:        ├──────────────┐
│                           ││ category_id = category_id │              │
│                           ││                           │              │
│        ~1,866 rows        ││        ~1,264 rows        │              │
└─────────────┬─────────────┘└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│           FILTER          ││       POSTGRES_SCAN       ││       POSTGRES_SCAN       │
│    ────────────────────   ││    ────────────────────   ││    ────────────────────   │
│    (line_type = 'SALE')   ││      Table: products      ││           Table:          │
│                           ││                           ││     product_categories    │
│                           ││        Projections:       ││                           │
│                           ││        product_code       ││        Projections:       │
│                           ││        category_id        ││        category_id        │
│                           ││                           ││       category_name       │
│                           ││                           ││                           │
│        ~1,866 rows        ││        ~1,264 rows        ││         ~148 rows         │
└─────────────┬─────────────┘└───────────────────────────┘└───────────────────────────┘
┌─────────────┴─────────────┐
│       READ_CSV_AUTO       │
│    ────────────────────   │
│         Function:         │
│       READ_CSV_AUTO       │
│                           │
│        Projections:       │
│        product_code       │
│         line_type         │
│            qty            │
│         unit_price        │
│                           │
│        ~9,331 rows        │
└───────────────────────────┘
┌──────────┬───────────────────┬───────────────────────┬────────────────────┐
│ store_id │    store_name     │     category_name     │      revenue       │
│ varchar  │      varchar      │        varchar        │       double       │
├──────────┼───────────────────┼───────────────────────┼────────────────────┤
│ S03      │ Annapurna T Nagar │ Staples & Grains      │ 1268461.3100000003 │
│ S03      │ Annapurna T Nagar │ Baby Care             │         1161403.37 │
│ S03      │ Annapurna T Nagar │ Edible Oils           │         1007056.36 │
│ S03      │ Annapurna T Nagar │ Dairy                 │ 519284.19999999995 │
│ S03      │ Annapurna T Nagar │ Personal Care         │ 474155.13000000006 │
│ S03      │ Annapurna T Nagar │ Frozen & Ready to Eat │ 406014.76000000007 │
│ S03      │ Annapurna T Nagar │ Beverages             │           374095.1 │
│ S03      │ Annapurna T Nagar │ Stationery & General  │          369826.79 │
│ S03      │ Annapurna T Nagar │ Home Care             │          353198.36 │
│ S03      │ Annapurna T Nagar │ Spices & Masala       │ 251832.33999999997 │
└──────────┴───────────────────┴───────────────────────┴────────────────────┘

========== PART (E) – CROSS-SYSTEM QUERY ==========

Sales data is stored in the MinIO object store, while
stores, products and product categories are stored in
PostgreSQL.

DuckDB was used as the analytical query engine. PostgreSQL
was attached as the database "pg", while the sales files
were read directly using READ_CSV_AUTO from the object store.

A single query joined the object-store sales data with:
- pg.public.stores
- pg.public.products
- pg.public.product_categories

No sales data was first copied into PostgreSQL.

The DuckDB EXPLAIN output shows READ_CSV_AUTO in the query
plan, providing evidence that the analytical engine evaluates
the object-store scan and performs the query.

========== PART (E) COMPLETE ==========

task f
month     finance_revenue   folder_revenue   difference
2024-01   38446071.33        38446071.33       0.00
2024-02   34887085.55        34887085.55       0.00
2024-03   42457899.09        41971649.09   486250.00
2024-04   37958457.37        37958457.37       0.00
2024-05   41764716.40        41764716.40       0.00
2024-06   38987082.82        38987082.82       0.00
2024-07   40527291.81        40295160.11   232131.70
2024-08   45252181.75        45252181.75       0.00
2024-09   44615037.46        44615037.46       0.00
2024-10   56359195.92        56359195.92       0.00
2024-11   51583838.47        51583838.47       0.00
2024-12   50745209.00        50745259.48     -50.48