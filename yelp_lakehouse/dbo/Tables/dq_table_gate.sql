CREATE TABLE [dbo].[dq_table_gate] (

	[critical_failed_rules] int NULL, 
	[layer] varchar(8000) NULL, 
	[major_failed_rules] int NULL, 
	[pipeline_run_id] varchar(8000) NULL, 
	[run_ts] datetime2(6) NULL, 
	[table_name] varchar(8000) NULL, 
	[total_rules] int NULL, 
	[dq_run_id] varchar(8000) NULL, 
	[passed_rules] int NULL, 
	[failed_rules] int NULL, 
	[decision] varchar(8000) NULL, 
	[decision_reason] varchar(8000) NULL
);