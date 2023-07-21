import r_lambda

from r_lambda.docker import docker_image

# python setup.py develop
# python tests/demo.py

# commandline test for docker
r_lambda.call_lambda(
    "demo::hello_world",
    argv={"str": "world", "raw": "/mnt/data/raw"},
    options=None,
    workdir="./",
    docker=docker_image(id="example_image", volumn=["/home","raw"], name="test"),
    run_debug=True,
)

# commandline test for bash
r_lambda.call_lambda(
    "demo::hello_world",
    argv={"str": "world", "raw": "/mnt/data/raw"},
    options=None,
    workdir="./",
    docker=None, # docker_image(id="example_image", volumn=["/home","raw"], name="test"),
    run_debug=True,
)