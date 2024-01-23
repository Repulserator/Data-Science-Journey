# xyz_Data_Assignment

I completed this assignment as part of an interview process for a company. It effectively demonstrates a fair portion of my skills, and hence, I wanted to include it.


## Problem 1: Data Modelling (related to Problem 2)
### Part 1
Uploaded is the file ERD.png

Details:

Considering the dynamic nature of customer details prone to change over time, I've refrained from imposing strict rules, although we should still maintain as much consistency as possible.

Regarding products, Each product has multiple variants, i personally think variants is much more important table. Products should maintain absolute consistency with the ids as primary key, The "variants" table should include product ID, variant ID, and status ID.

Then, I Introduced the "variant status" table to track the release and end dates of each product variant, allowing for multiple releases under different circumstances.

For orders, tracking prices, quantities, discounts, and status IDs, all details can be traced back to their respective tables for potential KPI calculations.


I have only ever done it on pen and paper before, this time i have taken the liberty to  use Illustrator


### Part 2

To generate data, I utilized various methods including manual entry, online generators, Python, and SQL. While the assessment primarily focuses on SQL, I acknowledged the need for a more diverse approach and generated a mock database to work with. I used python to generate an order history. You can find the implementation in pythonautogen.py.


I also took the care to randomly generate random price and discount in a range, also have different status for realism sake.

For variants and products, I created them manually.
For variant Status however, I developed an SQL script to automatically generate variants, with most having an end date set 10 years from now for validity. Check out Variants generator.sql for details


## Problem 2: SQL (related to Problem 1)

To enable future price analysis, I split prices details requiring extra multiplication and used temporary tables to get the final results - showing areas to improve my query skills. Similarly for customer spending analysis, I compared current and past years and categorized purchases to answer the requirements for now while noting opportunities to optimize the code later as I learn.


## Problem 3: ETL


Since I don't have much experience with JSON files, I had to resort to pandas documentation. I successfully loaded and organized the data into different tables, as documented in xyz json.ipynb. While the resulting structure doesn't necessarily reduce in size, I introduced subtables with ID, season, and orchestra name for grouping and reference. Attempts to nest them for better navigation proved unsuccessful. Facing challenges in comprehending certain aspects, I generated an ER diagram (ERD 2.png), suggesting that professional tools may be more fitting. The subsequent steps involve recreating the structures in Python and SQL, with the specifics of normalization and transformations remaining unclear.
