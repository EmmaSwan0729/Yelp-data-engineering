CREATE TABLE [dbo].[dq_run_log] (

	[dq_run_id] varchar(8000) NULL, 
	[pipeline_run_id] varchar(8000) NULL, 
	[layer] varchar(8000) NULL, 
	[table_name] varchar(8000) NULL, 
	[run_ts] datetime2(6) NULL, 
	[end_ts] datetime2(6) NULL, 
	[total_rules] int NULL, 
	[passed_rules] int NULL, 
	[failed_rules] int NULL, 
	[critical_failed_rules] int NULL, 
	[major_failed_rules] int NULL, 
	[final_decision] varchar(8000) NULL, 
	[status] varchar(8000) NULL, 
	[error_message] varchar(8000) NULL
);