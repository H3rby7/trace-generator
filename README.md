## Spår: Cluster Trace Generator

This command-line tool generates cluster trace in a more controllable manner based on [Alibaba's cluster trace](https://github.com/alibaba/clusterdata)

[![image](https://img.shields.io/pypi/l/spar.svg)](https://python.org/pypi/spar)
[![image](https://img.shields.io/pypi/pyversions/spar.svg)](https://python.org/pypi/spar)

## Requirements

Requires the data from Alibaba Cluster Trace 2018.

Requires [input sample files](./formats.md#input-format)

### Installation

Because [pickle](https://docs.python.org/3/library/pickle.html) has been used on scipy objects to create [distribution files](./spar/data/distributions/), we need the exact scipy version present to deserialize correctly.

```
pip install -r requirements.txt
```

### Usage

Within the root directory of this project (where this README.md resides.) we can use the tool by calling the `spar` python module as followed:

```
Usage: python -m spar [OPTIONS] OUTPUT_DIR

  By default, we output an hour-long trace from the original Alibaba
  trace to the OUTPUT_DIR. But you could provide several parameters
  and we would transform the trace as follows.
  1. Up- or down-sample trace according to load-factor. For up-sampling,
  we replace the dependencies with synthesized ones.
  1. Adjust resource heterogeneity according to heter-factor.
  2. Rescale resource request and usage according to machine-conf.

  Examples:

  Generate an <input-time-span>-long trace.
  $ python -m spar <OUTPUT_DIR>

  Generate an <input-time-span>-long trace with 2x jobs.
  $ python -m spar <OUTPUT_DIR> --load-factor 2

  Generate a half-<input-time-span>-long trace.
  $ python -m spar <OUTPUT_DIR> --duration 0.5

  Generate an hour-long trace with the resource request and usage deviating
  from the average 1.5x the original.
  $ python -m spar <OUTPUT_DIR> --heter-factor 1.5

  Generate an hour-long trace for clusters with 24 cores and 50 unit of memory.
  $ python -m spar <OUTPUT_DIR> --machine-conf (24, 50)

Options:
  --trace-dir PATH                The location of Alibaba trace.
  --load-factor FLOAT             A factor adjusting the average load (i.e., #
                                  jobs/hour) of the output trace.
  --duration FLOAT RANGE          The duration (in relation of the time spanning the sample data) of the trace.
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
