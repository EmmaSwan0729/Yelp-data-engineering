CREATE TABLE [dbo].[review_silver] (

	[review_id] varchar(8000) NULL, 
	[business_id] varchar(8000) NULL, 
	[user_id] varchar(8000) NULL, 
	[stars] float NULL, 
	[useful] bigint NULL, 
	[funny] bigint NULL, 
	[cool] bigint NULL, 
	[text] varchar(8000) NULL, 
	[date] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_batch_id] varchar(8000) NULL
);