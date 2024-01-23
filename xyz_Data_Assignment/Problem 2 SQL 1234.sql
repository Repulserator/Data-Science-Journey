--1. Retrieve the top 5 customers who have made the highest average order amounts in the last 6 months. 
--The average order amount should be calculated for each customer, and the result should be sorted in descending order.
USE [trial]
Go

Begin

--select MOCK_cust.custname,MOCK_ord.cust_id, AVG(price*quantity*(1-discount)) as avga, AVG(quantity) as quantity from MOCK_ord
select TOP 5 MOCK_cust.custname,MOCK_ord.cust_id, AVG(price*quantity*(1-discount)) as avga, AVG(quantity) as quantity from MOCK_ord
inner join MOCK_cust on MOCK_cust.custid = MOCK_ord.cust_id
where date >= DATEADD(Month, -6, GetDate())
Group By custname,cust_id
Order By avga DESC

End


--2 Retrieve the list of customer whose order value is lower this year as compared to previous year
Go
Begin
-- create 2 tables of this and last year
select MOCK_ord.cust_id, AVG(price*quantity*(1-discount)) as avgThis Into d2023Avg from MOCK_ord
inner join MOCK_cust on MOCK_cust.custid = MOCK_ord.cust_id
where date >= DATEADD(Year, 0, GetDate())
Group By cust_id

select MOCK_ord.cust_id, AVG(price*quantity*(1-discount)) as avglast Into d2022Avg from MOCK_ord
inner join MOCK_cust on MOCK_cust.custid = MOCK_ord.cust_id
where date >= DATEADD(Year, -1, GetDate())
Group By cust_id

--Join them and write it into a 3rd table
select d2023Avg.cust_id, avgThis, avglast into ddiff from d2023Avg
inner join d2022Avg on d2022Avg.cust_id = d2023Avg.cust_id


alter table ddiff
add diff float(32)

-- Create a new column to see the difference
update ddiff
set diff = avgThis - avglast

--See only the negative performings, sorted worst to best
select * from ddiff
where diff <=0
Order By diff ASC;

End




--Create a table showing cumulative purchase by a particular customer. Show the breakup of cumulative purchases by product category

USE [trial]
Go
Begin
-- Increment by Customer ID, since we are grouping by it, adn see the breakdown by category with inner joins
create table temptable2(customer_id int,cumulative_purchase float(32), Apparel float(32),Footwear float(32),Acc float(32))
declare @cid INT= 1;
While @cid<=10
Begin
SELECT
    cust_id, SUM(price*quantity*(1-discount)) AS cumulative_purchase,
	SUM(CASE WHEN Mock_prod.category = 'Apparel' THEN price*quantity*(1-discount) ELSE 0 END) as Apparel,
	SUM(CASE WHEN Mock_prod.category = 'Footwear' THEN price*quantity*(1-discount) ELSE 0 END) as Footwear,
    SUM(CASE WHEN Mock_prod.category = 'Accessories' THEN price*quantity*(1-discount) ELSE 0 END) as Acc
Into temptable
--For the life of me, could not figure out how to directly use aliases in inserts
FROM
    MOCK_ord
	inner join 
	MOCK_var on MOCK_var.variantid = Mock_ord.variant_id
	inner join 
	MOCK_prod on MOCK_prod.prodid = MOCK_var.prodid
WHERE
    cust_id = @cid
GROUP BY
    cust_id

--Since we can do 1, we can do 10, and used unions of temporary tables to retain the data. Since I have a deadline, i wont delve into this.

--CTE's were slowing me down considerably and hence i opted to use a more direct approach

-- The copy pasting bit
select * into dcumul
from temptable
UNION
select * from temptable2

drop table temptable2 

select * into temptable2 from dcumul

drop table dcumul
drop table temptable
-- The copy pasting bit

select * from temptable2
set @cid = @cid + 1;
End

End

select * from temptable2
select * from MOCK_ord
select * from MOCK_cust