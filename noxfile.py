import nox


@nox.session(python="3.8")
def lint(session):
    session.install("flake8", "flake8-black")
    session.run("flake8")


@nox.session(python="3.8")
def type(session):
    session.install("mypy")
    session.run("mypy")
