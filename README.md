## Spår: Cluster Trace Generator

This command-line tool generates cluster trace in a more controllable manner based on [Alibaba's cluster trace](https://github.com/alibaba/clusterdata)

[![image](https://img.shields.io/pypi/l/spar.svg)](https://python.org/pypi/spar)
[![image](https://img.shields.io/pypi/pyversions/spar.svg)](https://python.org/pypi/spar)

## Requirements

Requires [input sample files](./formats.md#input-format).
These csv files seem to be a mapped extract of their corresponding trace data files from alibaba 2018 trace.

### Installation

Because [pickle](https://docs.python.org/3/library/pickle.html) has been used on scipy objects to create [distribution files](./spar/data/distributions/), we need the exact scipy version present to deserialize correctly.

The `requirements.txt` has been created from `Pipfile.lock`, by running `pipenv requirements > requirements.txt`

Install dependencies:

```
pip install -r requirements.txt
```

### Usage

Within the root directory of this project (where this README.md resides.) we can use the tool by calling the `spar` python module as followed:

```
Usage: python -m spar [OPTIONS] OUTPUT_DIR

  By default, we output the sample_xxx.csv as they are to the OUTPUT_DIR.
  But you could provide several parameters to transform the trace as follows.
  1. Up- or down-sample trace according to load-factor. For up-sampling,
  we add synthesized jobs, while down-sampling drops jobs of the input sample.
  2. Adjust resource heterogeneity according to heter-factor.
  3. Rescale resource request and usage according to machine-conf.

  Examples:

  Output input trace as is.
  $ spar <OUTPUT_DIR>

  Output the input trace located in './input' directory.
  $ spar <OUTPUT_DIR> --trace-dir ./input

  Generate a trace of same lenght as the input with 2x jobs.
  $ spar <OUTPUT_DIR> --load-factor 2

  Generate a trace with half the length of the input trace.
  $ spar <OUTPUT_DIR> --duration 0.5

  Transforms the input trace with the resource request and usage deviating by 1.5x
  (on average) from the original resources.
  $ spar <OUTPUT_DIR> --heter-factor 1.5

  Transforms the input trace resource usage relative to the default machine config (96, 100).
  In this case requesting only 1/4 of the CPU and half the memory.
  $ spar <OUTPUT_DIR> --machine-conf (24, 50)

Options:
  --trace-dir PATH                The location of Alibaba trace.
  --load-factor FLOAT             A factor adjusting the average load of the
                                  output trace relative to the input trace.
  --duration FLOAT RANGE          The duration of the output trace relative to
                                  the input trace.
  --heter-factor FLOAT            A factor adjusting the heterogeneity
                                  (defined as the ratio: value/average) of the
                                  output trace.
  --machine-conf <INTEGER INTEGER>...
                                  An integer pair indicating the (CPU, memory)
                                  of each server. Default: (96, 100) as in
                                  Alibaba cluster.
  --help                          Show this message and exit.
```

### Publication

For more details, please refer to the following paper.

> Huangshi Tian, Yunchuan Zheng, and Wei Wang. "Characterizing and Synthesizing Task Dependencies of Data-Parallel Jobs in Alibaba Cloud." In SoCC. 2019.


### Contributing

Any form of contribution is welcome! If you find a bug, create an issue; if you extend a feature, send a pull request.


### Acknowledgement

[@SimonZYC](https://github.com/SimonZYC) has significantly contributed to this project.
