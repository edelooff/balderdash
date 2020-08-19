import nox


@nox.session(python="3.8")
def lint(session):
    session.install("flake8", "flake8-black", "flake8-isort")
    session.run("flake8")


@nox.session(python="3.8")
def type(session):
    session.install("mypy")
    session.run("mypy")


@nox.session(python="3.8")
def test(session):
    session.install("pytest", "pytest-cov", "coverage[toml]")
    session.install(".")
    session.run("python", "-m", "pytest", "--cov")
