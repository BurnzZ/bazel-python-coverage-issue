workspace(name = "rules_python_pip_parse_example")

local_repository(
    name = "rules_python",
    path = "../..",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")
py_repositories()
python_register_toolchains(
    name = "python_3_9",
    python_version = "3.9.13",
)

load("@rules_python//python:pip.bzl", "pip_parse")
pip_parse(
    name = "pypi",
    python_interpreter_target = "@python_3_9_host//:python",
    requirements_lock = "requirements_lock.txt",
    requirements_windows = "requirements_windows.txt",
)

load("@pypi//:requirements.bzl", "install_deps")
install_deps()
