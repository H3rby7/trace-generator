# coding: utf-8
import random
from math import ceil, floor
from pathlib import Path

import click

from .io import iter_job, write_job
from .progress import Bar
from .generate import random_interval, random_job
from .transform import Transformer


@click.command()
@click.argument('output-dir', type=click.Path(exists=True))
@click.option('--trace-dir', type=click.Path(exists=True), default=(Path(__file__).parents[0] / 'data' / 'samples'),
              help='The location of Alibaba trace.')
@click.option('--load-factor', type=float, default=1,
              help='A factor adjusting the average load of the output trace relative to the input trace.')
@click.option('--duration', type=click.FloatRange(0, None), default=1,
              help='The duration of the output trace relative to the input trace.')
@click.option('--heter-factor', type=float, default=1,
              help='A factor adjusting the heterogeneity (defined as the ratio: value/average) of the output trace.')
@click.option('--machine-conf', type=(int, int), default=(96, 100),
              help='An integer pair indicating the (CPU, memory) of each server. Default: (96, 100) as in Alibaba cluster.')
def main(trace_dir, output_dir, load_factor, heter_factor, machine_conf, duration):
    '''
    \b
    By default, we output the sample_xxx.csv as they are to the OUTPUT_DIR.
    But you could provide several parameters to transform the trace as follows.
    1. Up- or down-sample trace according to load-factor. For up-sampling,
    we add synthesized jobs, while down-sampling drops jobs of the input sample.
    2. Adjust resource heterogeneity according to heter-factor.
    3. Rescale resource request and usage according to machine-conf.

    Examples:

    \b
    Output input trace as is.
    $ spar <OUTPUT_DIR>

    \b
    Output the input trace located in './input' directory.
    $ spar <OUTPUT_DIR> --trace-dir ./input

    \b
    Generate a trace of same lenght as the input with 2x jobs.
    $ spar <OUTPUT_DIR> --load-factor 2

    \b
    Generate a trace with half the length of the input trace.
    $ spar <OUTPUT_DIR> --duration 0.5

    \b
    Transforms the input trace with the resource request and usage deviating by 1.5x
    (on average) from the original resources.
    $ spar <OUTPUT_DIR> --heter-factor 1.5

    \b
    Transforms the input trace resource usage relative to the default machine config (96, 100).
    In this case requesting only 1/4 of the CPU and half the memory.
    $ spar <OUTPUT_DIR> --machine-conf (24, 50)
    '''
    with (Path(trace_dir) / 'sample_tasks.csv').open() as sample_task, \
         (Path(trace_dir) / 'sample_instances.csv').open() as sample_instance, \
         (Path(output_dir) / 'batch_task.csv').open('w') as output_task, \
         (Path(output_dir) / 'batch_instace.csv').open('w') as output_instace:

        # Just to have a clearer name for 'duration' throughout the code, as it means the trace's total duration, not a job duration.
        stretch_factor = duration

        # Relative to the count of jobs in the input samples
        job_factor = stretch_factor * load_factor

        transformer = Transformer(heter_factor, machine_conf)
        output_job = lambda a, j: write_job(a, transformer.transform(j),
                                            output_task, output_instace)
        
        # the arrival time of the previously generated job
        prev_job_arrival = 0

        total_jobs = 16749 * job_factor  # total number of jobs to be generated
        step_size = int(30 * random.random() + 20)  # enlarge interval of updating progress bar to reduce overhead
        with Bar(label='Generating jobs ', expected_size=total_jobs, every=step_size) as bar:
            # Iterate over input samples
            for i, (arrive_at, job) in enumerate(iter_job(sample_task, sample_instance)):
                insert_sample_job = False
                if job_factor == 1:
                    # We need exactly the amount of jobs we have in our sampleset
                    insert_sample_job = True

                elif job_factor > 1:
                    # We need more jobs than we have
                    # We fill up by chance using synthesized jobs.
                    insert_sample_job = True
                    # How many synthesized jobs we need (we subtract '1' as we will add the sample job for sure.)
                    synthesized_jobs = job_factor - 1
                    # As we cannot insert fractions of a job, we either overcommit (ceil(value)) or undercommit (floor(value))
                    to_insert = ceil(synthesized_jobs) if floor(synthesized_jobs) + random.random() < synthesized_jobs else floor(synthesized_jobs)
                    # Use previous job's arrival time as reference point
                    synth_job_arrival = prev_job_arrival
                    for _ in range(to_insert):
                        # Calculate synthesized job arrival time
                        synth_job_arrival += random_interval() / load_factor
                        output_job(synth_job_arrival, random_job())

                # We need less jobs than our sampleset
                # So we only retain the job by chance
                elif random.random() < job_factor:
                    insert_sample_job = True

                # Calculate arrival time of job using the stretch factor
                stretched_job_arrival = arrive_at * stretch_factor

                if insert_sample_job:
                    # Only add job if needed
                    output_job(stretched_job_arrival, job)

                # Save arrival time of the possibly created job.
                prev_job_arrival = stretched_job_arrival

                bar.show(int(i * job_factor))


if __name__ == '__main__':
    main()
