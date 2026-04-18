CREATE TABLE [dbo].[dq_table_gate] (

	[dq_run_id] varchar(8000) NULL, 
	[pipeline_run_id] varchar(8000) NULL, 
	[run_ts] datetime2(6) NULL, 
	[layer] varchar(8000) NULL, 
	[table_name] varchar(8000) NULL, 
	[total_rules] bigint NULL, 
	[passed_rules] bigint NULL, 
	[failed_rules] bigint NULL, 
	[critical_failed_rules] bigint NULL, 
	[major_failed_rules] bigint NULL, 
	[decision] varchar(8000) NULL, 
	[decision_reason] varchar(8000) NULL
);