# Tutorial 1: CodaLab Basics with GLUE Benchmarks

--------------------------------------------------------------------------------

**Estimated Time:** 30-45 min

This tutorial provides an overview of how to set up CodaLab and use it for
performing experiments and sharing results.

We'll train some models to tackle the MNLI (Multi-Genre Natural Language Inference) 
task, drawn from the GLUE (General Language Understanding Evaluation) benchmark:

```
@InProceedings{conneau2017infersent,
  author    = {Conneau, Alexis  and  Kiela, Douwe  and  Schwenk, Holger  and  Barrault, Lo\"{i}c  and  Bordes, Antoine},
  title     = {Supervised Learning of Universal Sentence Representations from Natural Language Inference Data},
  booktitle = {Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing},
  month     = {September},
  year      = {2017},
  address   = {Copenhagen, Denmark},
  publisher = {Association for Computational Linguistics},
  pages     = {670--680},
  url       = {https://www.aclweb.org/anthology/D17-1070}
}
```

## 1. Setting up the tutorial

### 1.1 Create a new worksheet

- Sign up for a CodaLab account at [https://worksheets.codalab.org/](https://worksheets.codalab.org/),
  if you don't have one already.
- After signing in, click "My Dashboard". On this screen, you can see summary of the
  bundles and worksheets you create.
- We're going to create a new worksheet to track our results from this tutorial,
  so click "New Worksheet" and name it something like `<username>-tutorial-01`.

### 1.2 Install the CLI tool

- The command line interface (CLI) allows you to interact with the central
  CodaLab server (where your worksheets are stored) from your local terminal.
- Make sure you have the necessary dependencies (Python 2.7, setuptools, virtualenv, fuse).
- Install the CLI by running:
  ```
    pip install codalabworker
    pip install codalab
  ```
  You should now be able to use the `cl` command in your terminal.
- Initialize the CLI by running:
  ```
  cl work
  ```
  Log in with your CodaLab account username and password.
- Switch the current worksheet context to the new worksheet you created:
  ```
  cl work main::<username>-tutorial-01
  ```
  
### 1.3 Initialize the environment and data
  
  - Navigate to the `01-glue/` directory and run `bash ./setup.sh`. This script will:
      - create a virtual environment `venv` for this tutorial
      - download the MNLI dataset (~312 MB zipped) into a subdirectory called `data/`
      - create `experiments/` directory for saving results
  - Activate the virtual environment: `source venv/bin/activate`

## 2. Working with datasets

### 2.2 Upload a data bundle

- One option for working with datasets is to upload your own.
- Since `data/MNLI` is already prepared for you, we can upload it so that we can later use it
to run experiments:
  ```
  cl upload data/MNLI -d "Multi-Genre Natural Language Inference dataset from (Williams et al. 2016)."
  ```
- Let's see this bundle in the online worksheet. Go to "My Dashboard" and click on the
  tutorial for this worksheet. You should be able to see the new data bundle in the sheet.

### 2.3 Use an existing data bundle

- Another option for working with datasets is to use an existing public dataset that others
  have shared.
- We're going use pretrained GloVe vectors from a public worksheet titled
  `word-vectors`. To search for this worksheet, type `wsearch word-vectors` in the
  online console, and click on the bundle with the UUID of `0xc946df`. It should take you
  to [this worksheet](https://worksheets.codalab.org/worksheets/0xc946dfbd2215486493672a5e5b0c88d8/),
  where you can see the various data bundles with common word vector datasets.
- Later, we'll be able to directly *depend on* bundles from this worksheet to
  run our code.

## 3. Writing your code

### 3.1 Use JSON to easily display results

- CodaLab allows you to work with all kinds of files and formats. When you execute a run,
  a *run bundle* is created that stores the files that were created, as well ast
  standard out/err.
- But there are some special formats that you can output your results in order to easily
  display them in the worksheet. We're going to set up JSON output.
- Notice that our code in [main.py](01-glue/main.py#L1-5) outputs its results in a file
  called `results.json`. Currently, the JSON file has the following shape (**TODO**):
  ```json
  {
      train_accuracy: number,
      train_F1: number,
      dev_accuracy: number,
      dev_F1: number
  }
  ```
- We'll be able to use *directives* to automatically add these results to a table in our
  worksheet so that we can track our results.
- Read up on how to use Markdown directives in a worksheet:
  [Worksheet Markdown](https://github.com/codalab/codalab-worksheets/wiki/Worksheet-Markdown#directives)
- In order to display the results from our run, paste the following schema in your worksheet:
  ```
  % schema simple1
  % add uuid uuid [0:8]
  % add name
  % add train_accuracy /output/results.json:train_accuracy
  % add train_F1 /output/results.json:train_F1
  % add dev_accuracy /output/results.json:dev_accuracy
  % add dev_F1 /output/results.json:dev_F1
  ```

### 3.2 Use a run script for convenience

- It's possible to manually call `cl run` for each run you want to make. But in practice,
  many researchers use a *run script* to speed things up and avoid repition / mistakes.
- Check out the provided [run.sh](./run.sh) which we will use to run our commands.

## 4. Running on CodaLab

### 4.1 Run an experiment

- TODO: Use run script

### 4.2. Run another experiment

- TODO: Make changes, run again

## 5. Share your results

- TODO: Change permissions
