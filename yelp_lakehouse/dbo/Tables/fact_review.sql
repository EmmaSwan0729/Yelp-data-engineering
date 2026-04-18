CREATE TABLE [dbo].[fact_review] (

	[review_id] varchar(8000) NULL, 
	[business_id] varchar(8000) NULL, 
	[user_id] varchar(8000) NULL, 
	[date_id] int NULL, 
	[stars] float NULL, 
	[useful] bigint NULL, 
	[funny] bigint NULL, 
	[cool] bigint NULL, 
	[_ingest_ts] datetime2(6) NULL
);