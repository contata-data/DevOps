CREATE OR REPLACE PROCEDURE `relevate-dev-403605.RelevateSystem.DevOpsTest_Proc`(id_ int64)
BEGIN
select Id, Name  FROM RelevateSystemStaging.DevOpsTest where id=id_ ;
END; 