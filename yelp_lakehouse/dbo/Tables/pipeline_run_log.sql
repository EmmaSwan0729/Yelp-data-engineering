CREATE TABLE [dbo].[pipeline_run_log] (

	[pipeline_run_id] varchar(8000) NULL, 
	[pipeline_name] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[table_name] varchar(8000) NULL, 
	[status] varchar(8000) NULL, 
	[start_time] datetime2(6) NULL, 
	[end_time] datetime2(6) NULL, 
	[input_rows] bigint NULL, 
	[output_rows] bigint NULL, 
	[dq_status] varchar(8000) NULL
);