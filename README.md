# CodaLab Worksheets: Tutorials & Examples

This repo contains tutorials and examples to get you up and rolling with conducting experiments and sharing results with CodaLab Worksheets.

You can get started with the tutorial by cloning the repository: 

    git clone https://github.com/codalab/worksheets-examples

Please watch this video to understand the problems that CodaLab seeks to solve:
https://www.youtube.com/watch?v=WwFGfgf3-5s

# Overview

There are two important concepts in CodaLab: bundles and worksheets.

## Bundles

Bundles are immutable files/directories that represent the code, data, and results of an experimental pipeline. There are two ways to create bundles:

1.  Users can directly upload either **a single file or a folder** as a bundle. This can contain a dataset in any format or programs in any programming language.
2.  Users can create what is called a **run bundle** by executing a shell command that depend on the contents of other bundles. This shell command is executed in a Docker container in a directory with the dependencies mounted as readonly files. When the shell command finishes executing, the run bundle consists of the files/directories which were written to the current directory by the shell command.

<img src="https://github.com/codalab/codalab-worksheets/wiki/images/execution.png" />

Above, each green rectangle represents a bundle, while arrows represent dependencies. The top left bundle is a single script uploaded as a bundle, `cnn.py`, while the top right bundle is a folder `mnist` which contains two files.

`cnn.py` and `mnist` are dependencies of `exp2`, which is a run bundle. The box on the right shows the file structure within the Docker container that is running `exp2`, as well as the shell command that is being executed (bottom of box in green). We can see that after the `exp2` is done running, only `stdout`, `stderr`, and `stats.json` get saved, since the other files/folders were mounted as dependencies from other bundles.

This dependency graph of bundles precisely captures the research process in an immutable way.

## Worksheets

Worksheets organize and present an experimental pipeline in a comprehensible way, and can be used as a lab notebook, a tutorial, or an executable paper. Worksheets contain references to bundles, and are written in a **custom markdown language**.

As an example, the figure below shows an abstract dependency graph over four bundles in the center. On the side are two separate worksheets, which contain both text and pointers to various bundles. Worksheet 1 might be Percy's worksheet where he is running experiments for his own project, while Worksheet 2 might be Kerem's project where he compares Percy's project (bundle 0x19) against someone else's (bundle 0xe1).

<img src="https://github.com/codalab/codalab-worksheets/wiki/images/worksheets-schema.png" />

CodaLab's philosophy is to give you full control of how you want to run your experiments and get out of your way, while providing a platform where you can easily keep track of the experiments that you've ran. You should be able to use the same tools, programming languages, and shell scripts that you do during your normal workflow. A good analogy is Git, which just maintains the revision history and gives you total freedom in terms of what to put in your repository.


## Table of Contents

0.  [Quickstart](00-quickstart/README.md) -
    Learn the basics of the CodaLab workflow of uploading files and executing code on CodaLab. 
1.  [Workflow Basics](01-basics/README.md) -
    Familiarize yourself with the CodaLab workflow by runing some simple experiments using the SNLI dataset.
