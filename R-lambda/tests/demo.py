import r_lambda

from r_lambda.docker import docker_image

# python setup.py develop
# python tests/demo.py

r_lambda.call_lambda(
    "demo::hello_world",
    argv={"str": "world"},
    options=None,
    workdir="./",
    docker=docker_image(id="example_image", volumn=["/home"], name="test"),
    run_debug=True,
)
