CREATE TABLE [dbo].[checkin_silver] (

	[business_id] varchar(8000) NULL, 
	[date] varchar(8000) NULL, 
	[_ingest_ts] datetime2(6) NULL, 
	[_source_file] varchar(8000) NULL, 
	[_batch_id] varchar(8000) NULL
);