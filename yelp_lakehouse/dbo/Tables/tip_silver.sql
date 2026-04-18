CREATE TABLE [dbo].[tip_silver] (

	[user_id] varchar(8000) NULL, 
	[business_id] varchar(8000) NULL, 
	[text] varchar(8000) NULL, 
	[date] varchar(8000) NULL, 
	[compliment_count] int NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_batch_id] varchar(8000) NULL
);