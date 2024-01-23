-- 

USE [trial]
GO

Declare @var as INT = 2002;
While(@var<2031)
Begin
declare @result nvarchar(10) = (SELECT CONCAT('V', @var));
set @var = @var + 1;
declare @res int = (select MAX(statusid) from Mock_variantstatus)
Print @result
INSERT INTO Mock_variantstatus
           (statusid
           ,variantid
           ,launchdate
           ,enddate)
     VALUES
           (@res+1,@result,'2021-01-01','2030-12-12')
End
GO