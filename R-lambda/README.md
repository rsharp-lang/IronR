# Run ``R#`` lambda function in python workflow

## Introduce the ``R#`` lambda

The ``R#`` lambda function is a kind of shell feature function in R# script host. Assuming that there is a function named ``hello_world`` in a ``R#`` package which is named ``demo``, so that we could run this hello world function in R# script file:

```r
# function inside package namespace: demo 
const hello_world = function(str) {
    print(`hello: ${str}!`);
}

# call function in another script file
demo::hello_world("world");
```

Via the ``R#`` lambda function feature, that we could run this function without write script file, and we could run this function from commandline directly, example as:

```bash
# call function via R# lambda
Rscript --lambda demo::hello_world
```

and the parameter value of hello world function will be setup via a runtime json file ``./.r_env/run.json`` in the working directory:

```json
{
    "str": "world" 
}
```

If the function invoke contains ``getOption`` function calls, then you could setup the runtime environment via the json file ``./.r_env/options.json`` in the working directory:

```json
{
    "example-var": "1234"
}
```

So, you could get such environment variable value in R# runtime environment by ``getOption``:

```r
print(getOption("example-var"));
# [1] "1234"
```

## Call R# lambda from a python workflow

For call a R# lambda function from your python workflow, then you could use this python package function. Current package call the R# workflow function running in local machine or running in a docker container already been wrapped into function calls, so that you can call such hello world function in ``R#`` package in python, example like:

```py
import r_lambda
from r_lambda.docker import docker_image

r_lambda.call_lambda("demo::hello_world", 
argv = {"str": "world"}, 
    options = None,
    workdir = "./",
    docker = docker_image(id = "example_image", 
        volumn = ["/home"], name = "test"), 
    run_debug = False
)
```
