CREATE TABLE [dbo].[dim_date] (

	[date_id] int NULL, 
	[date] varchar(8000) NULL, 
	[year] int NULL, 
	[quarter] int NULL, 
	[month] int NULL, 
	[day] int NULL, 
	[weekofyear] int NULL, 
	[dayofweek] int NULL, 
	[day_name] varchar(8000) NULL
);