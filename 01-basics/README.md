# Tutorial 1: Workflow Basics

--------------------------------------------------------------------------------

**Estimated Time:** 30-45 min

This tutorial provides an overview of how to set up CodaLab and use it for
performing experiments and sharing results.

We'll train some models to tackle the SNLI (Stanford Natural Language Inference) task from:

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

The source code in this tutorial has been adapted from the real research repo, found at:
[facebookresearch/InferSent](https://github.com/facebookresearch/InferSent).

## 1. Setting up

### 1.1 Create a new worksheet

- Sign up for a CodaLab account at [https://worksheets.codalab.org/](https://worksheets.codalab.org/),
  if you don't have one already.
- After signing in, click "My Dashboard". On this screen, you can see summary of the
  bundles and worksheets you create.
- We're going to create a new worksheet to track our results from this tutorial,
  so click "New Worksheet" and name it something like `<username>-01-basics`.

### 1.2 Install the CLI tool

- The command line interface (CLI) allows you to interact with the central
  CodaLab server (where your worksheets are stored) from your local terminal.
- Make sure you have the necessary dependencies (Python 2.7, setuptools, virtualenv, fuse).
- Install the CLI by running:
  ```
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
  cl work main::<username>-01-basics
  ```
  
### 1.3 Initialize the environment and data
  
  - Navigate to the `01-basics/` directory and run `bash ./setup.sh`. This script will:
      - create a virtual environment `venv` for this tutorial
      - download the SNLI dataset (~69 MB unzipped) into `datasets/`
  - Activate the virtual environment: `source venv/bin/activate`

## 2. Working with datasets

### 2.1 Upload a bundle with data

- One option for working with datasets is to upload your own.
- Since `datasets/SNLI` has been prepared for you, we can upload it so that we can later use it
to run experiments:
  ```
  cl upload datasets/SNLI -d "Stanford Natural Language Inference dataset from (Bowman et al. 2015)."
  ```
- Let's see this bundle in the online worksheet. Go to "My Dashboard" and click on the
  tutorial for this worksheet. You should be able to see the new data bundle in the worksheet.

### 2.2 Use an existing data bundle

- Another option for working with datasets is to use an existing public dataset that others
  have shared.
- We're going use pretrained GloVe vectors from a public worksheet titled
  `word-vectors`. To search for this worksheet, type `wsearch word-vectors` in the
  online console, and click on the bundle with the UUID of `0xc946df`. It should take you
  to the ["Pretrained Word Vectors" worksheet](https://worksheets.codalab.org/worksheets/0xc946dfbd2215486493672a5e5b0c88d8/),
  where you can see the various data bundles with common word vector datasets.
- Add this bundle to our worksheet by running (**TODO**):
  ```
  cl add bundle word-vectors//glove.840B.300d .
  ```
- Later, we'll be able to directly *depend on* bundles from this worksheet to
  run our code.

## 3. Running your code

### 3.1 Upload a bundle with code

- We're now going to upload our code:
  ```
  cl upload src/ -d "Infersent source code from (Conneau et al. 2017)."
  ```

### 3.2 Use a run script for convenience

- It's possible to manually call `cl run` for each run you want to make. But in practice,
  many researchers use a *run script* to speed things up and avoid repition / mistakes.
- Check out the provided [run.sh](./run.sh) which we will use to assemble our commands.
- Now, let's run actually run our code!
  ```
  bash train.sh
  ```
- Go to the online worksheet, and track the progress of your run.

### 3.3 Use JSON to easily display results

- CodaLab allows you to work with all kinds of files and formats. When you execute a run,
  a *run bundle* is created that stores the files that were created, as well ast
  standard out/err.
- But there are some special formats in which you can output your results so that you can easily
  display them in the worksheet. In this case, we've set up JSON output for our results.
- Notice that the run bundle outputs its results in a file called `results.json` with the following shape (**TODO**):
  ```json
  {
      train_acc: number,
      dev_acc: number,
      test_acc: number,
  }
  ```
- We'll be able to use *directives* to automatically add these results to a table in our
  worksheet so that we can track our results.
- Read up on how to use Markdown directives in a worksheet:
  [Worksheet Markdown](https://github.com/codalab/codalab-worksheets/wiki/Worksheet-Markdown#directives)
- In order to display the results from our run, paste the following schema in your worksheet:
  ```
  % schema infersent
  % add uuid uuid [0:8]
  % add name
  % add train_accuracy /output/results.json:train_acc
  % add dev_accuracy /output/results.json:dev_acc
  ```

## 4. Performing experiments

### 4.1 Run with different parameters

- In your local environment, change the parameters of your run by updating the main run command in
  `train.sh` to the following:
  ```
  CMD="$CMD 'python src/train_nli.py \
           --word_emb_path datasets/GloVe/glove.840B.300d.txt \
           --encoder_type LSTMEncoder
           --train_frac 0.1'"
  ```
  Feel free to change other parameters to try to improve the model accuracy. Look at `src/train_nli.py` for
  a list of possible pararameters to change.
- Then, run `train.sh` again and see the results in the worksheet.

### 4.1 Run with different code

- TODO: Change model

## 5. Share your results

- When you are done adding to your worksheet and making it look nice, you're ready to share it with
  the world.
- In the online interface for the worksheet, you should see that the permissions are set to
  `permissions: you(all) public(read)`.
  This means that you can just share the URL of your worksheet, and the public will be able to see it.
  It's that simple!

**Congratulations**, you're done with the "Workflow Basics" tutorial!
