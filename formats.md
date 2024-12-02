# Trace Format

## Output Format

### Directory Structure

The output of the tool is shown below. <OUTPUT_DIR> is the argument specified by the user.

<OUTPUT_DIR>
├── batch_instances.csv  # detailed information of instances
└── batch_tasks.csv      # that of tasks

### Output Trace Format

In batch_tasks.csv, each line contains the following columns:

    job arrival time (in seconds)
    job name
    task name: the suffix separated by _ represents the dependency
    duration
    requested CPU: every 100 unit means 1 core
    requested memory: the fraction of 100 unit
    number of instances

Each line in batch_instance.csv consists of:

    job arrival time (in seconds)
    job name
    task name
    instance name
    duration
    average used CPU
    average used memory

For more explanation, please refer to the schema in Alibaba trace.


## Input Format

The tool comes with an hour-long sample trace extracted from the original Alibaba one. But users can provide their own where our tool can adjust trace length, average load, etc.

### Input Directory Structure

The <TRACE_DIR> is the parameter provided by the user, and it should contain two files.

<TRACE_DIR>
├── sample_instances.csv  # detailed information of instances
└── sample_tasks.csv      # that of tasks

### Input Trace Format

The trace has the same format as the output, but it has several ordering constraint:

    Both traces should be in the ascending order of arrival time.
    Within the same arrival time, the traces should be ordered by job name.
    In the same job, the traces should be ordered by task name.
