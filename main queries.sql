
select * from vacancy
WHERE vacancy.lastdate not in (
   SELECT lastdate FROM vacancyold)


select * from vacancy where sallary = (select max(sallary) from vacancy)