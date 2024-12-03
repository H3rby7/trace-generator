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
    number of instances (this will corelate with its entries in batch_instance.csv)

Each line in batch_instance.csv consists of:

    job arrival time (in seconds)
    job name
    task name
    instance name
    duration
    average used CPU
    average used memory

For more explanation, please refer to the 
[schema](https://github.com/alibaba/clusterdata/blob/7358bbaf40778d4bd0464a64a430812088b7b74e/cluster-trace-v2018/schema.txt)
in the
[Alibaba trace](https://github.com/alibaba/clusterdata/blob/7358bbaf40778d4bd0464a64a430812088b7b74e/cluster-trace-v2018/trace_2018.md).

## Input Format

Users have to provide their sample input (see below). The tool can adjust trace length, average load, etc.

The pip-version of the tool comes with an hour-long sample trace extracted from the original Alibaba one (https://github.com/All-less/trace-generator/issues/10#issuecomment-1464038206).

After installation of the tool via `pip install spar` the data resides at:

    /usr/local/lib/python3.7/site-packages/spar/data/samples/*

You may copy these files, or simply run the tool once without extra args, as it will simply output the input trace that way.

### Input Directory Structure

The <TRACE_DIR> is the parameter provided by the user, and it should contain two files.

    <TRACE_DIR>
    ├── sample_instances.csv  # detailed information of instances
    └── sample_tasks.csv      # detailed information of tasks

### Input Trace Format

The trace has the same format as the output, but it has several ordering constraints:

* Both traces should be in the ascending order of arrival time.
* Within the same arrival time, the traces should be ordered by job name.
* In the same job, the traces should be ordered by task name.
