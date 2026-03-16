CREATE TABLE [dbo].[pipeline_run_log] (

	[pipeline_run_id] varchar(8000) NULL, 
	[pipeline_name] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[target_table] varchar(8000) NULL, 
	[status] varchar(8000) NULL, 
	[start_ts] datetime2(6) NULL, 
	[end_ts] datetime2(6) NULL, 
	[duration_sec] float NULL, 
	[dq_run_id] varchar(8000) NULL, 
	[dq_status] varchar(8000) NULL, 
	[dq_checked_table] varchar(8000) NULL, 
	[input_rows] bigint NULL, 
	[output_rows] bigint NULL, 
	[error_message] varchar(8000) NULL, 
	[created_at] datetime2(6) NULL
);