# Account Creation / Installation

1.  Go to http://worksheets.codalab.org, and click "Sign Up" in the top-right corner:
2.  Fill out the subsequent form, and then submit the form using the "Sign Up" bottom in the bottom of the screen.
3.  A verification email will be sent to the email address you used to sign up. When you open it, there will be a link to follow in order to verify your account.
4.  After verifying your account, sign in again. This will bring you to "My Dashboard". This is a **special, read-only worksheet** that contains an overview of your activity and documents on Codalab. You can get back to this page at any time by clicking the "My Dashboard" button in the top-right.

![Dashboard screenshot](https://raw.githubusercontent.com/codalab/worksheets-examples/glue-tutorial/00-quickstart/dashboard.png)

5.  Click on the "My Home" button in the top right. This will bring you to your **home worksheet**. This worksheet is yours to customize, and has a name with format "home-<your username>".

![Dashboard screenshot](https://raw.githubusercontent.com/codalab/worksheets-examples/glue-tutorial/00-quickstart/home.png)

Next, we will install the CodaLab CLI. You can do this by running the following commands in your command line (assuming python and pip are installed).

    $ pip install codalab -U

    Collecting codalab
      Downloading https://files.pythonhosted.org/packages/56/3c/70f441cbb7e6df0cc667d6f924d797638c72e853f24ef013473ca6dc1d20/codalab-0.2.37.tar.gz (190kB)
        100% |████████████████████████████████| 194kB 6.5MB/s 
    ...


Alternatively, if you are in the Stanford NLP group, you can ssh into the NLP cluster, where the CodaLab CLI should already be installed.

# Quickstart

First, navigate to the same directory as this README (`worksheets-examples/00-quickstart`). We'll be walking through using the basic CodaLab commands and their functionality. 

`cl work` will prompt you for your user name and password into CodaLab, as well as tell you what your current working worksheet is. Below is the output for logging into the `test` account. 

    worksheets-examples/00-quickstart$ cl work
    Requesting access at https://worksheets.codalab.org
    Username: test
    Password: 
    Currently on worksheet https://worksheets.codalab.org::home-test(0x39729afdca6140869a11e055e4cc0649).

## Setting up a worksheet

Let's create a new worksheet called "quickstart-<username>", since worksheets must have a unique name. This will print out the UUID of the new worksheet. We can then make this new worksheet our current working worksheet. 

    worksheets-examples/00-quickstart$ cl new quickstart-test
    0xd9975e25878346f8ac8d369e7e3153c9
    worksheets-examples/00-quickstart$ cl work quickstart-test
    Switched to worksheet https://worksheets.codalab.org::quickstart-test(0xd9975e25878346f8ac8d369e7e3153c9).

Next, we'll upload the `data` and `code` folders with the following contents, respectively:

`data/lines.txt`:

    my
    first
    tutorial

`code/sort.py`

    import sys
    for line in sorted(sys.stdin.readlines()):
    	print line,

The following commands will zip up each directory and upload them as bundles, with bundle names "simple-data" and "simple-code" respectively. `cl up` will zip up the directory, upload it to codalab, and then output the bundle's UUID. We use the `-n` parameter to specify a bundle name; if no name is specified, then the name of the bundle will be the name of the directory. 

    worksheets-examples/00-quickstart$ cl up data -n quickstart-data
    Preparing upload archive...
    Uploading data.tar.gz (0x47041bd9565941f38a001b705a90c502) to https://worksheets.codalab.org
    Sent 0.00MiB [0.00MiB/sec]              
    0x47041bd9565941f38a001b705a90c502
    worksheets-examples/00-quickstart$ cl up code -n quickstart-code
    Preparing upload archive...
    Uploading code.tar.gz (0xb536a6447bbe4ec797054d38667384ce) to https://worksheets.codalab.org
    Sent 0.00MiB [0.00MiB/sec]              
    0xb536a6447bbe4ec797054d38667384ce

## Running a worksheet
Here, we're going to execute our sorting code on the `lines.txt` file. We'll mount the `quickstart-data` and `quickstart-code` bundles as dependencies, by prepending a colon before them. Dependencies are mounted onto the root of the file system with their bundle name. We again use the `-n` parameter to name the bundle that represents this run. 

    worksheets-examples/00-quickstart$ cl run :quickstart-data :quickstart-code "python quickstart-code/sort.py << quickstart-data/lines.txt" -n sorted
    0xea46dbb112444eb1aba285623cbe433f

To see the output of the bundle after you run it, you can see the files within the bundle with `cl cat sorted`, and the standard output with `cl cat sorted/stdout`. 
