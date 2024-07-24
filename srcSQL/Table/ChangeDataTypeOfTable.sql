-- Change data type of a column
-- Step 1: Create table with the changed data type
-- Changing data type of Id from INT to STRING
create table relevate-dev-403605.RelevateSystemStaging.DevOpsTest_DataType
(
  Id String
  ,Name STRING
);

-- Step 2: Insert data into the new table with the changed data type
Insert into  relevate-dev-403605.RelevateSystemStaging.DevOpsTest_DataType
(Id,Name)
select Cast(Id as String) as Id,Name FROM relevate-dev-403605.RelevateSystemStaging.DevOpsTest;

-- Step 3: Drop the original table with the old data type
Drop table relevate-dev-403605.RelevateSystemStaging.DevOpsTest;

-- Step 4: Clone the new table back to the original table name
Create table relevate-dev-403605.RelevateSystemStaging.DevOpsTest Clone 

 relevate-dev-403605.RelevateSystemStaging.DevOpsTest_DataType