CREATE TABLE [dbo].[review_bronze] (

	[business_id] varchar(8000) NULL, 
	[cool] bigint NULL, 
	[date] varchar(8000) NULL, 
	[funny] bigint NULL, 
	[review_id] varchar(8000) NULL, 
	[stars] float NULL, 
	[text] varchar(8000) NULL, 
	[useful] bigint NULL, 
	[user_id] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_batch_id] varchar(8000) NULL
);