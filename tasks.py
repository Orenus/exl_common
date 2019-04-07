from invoke import task
import os

####### PUBLISH ########################
# invoke publish -r exl_nexus_dev
# invoke publish exl_nexus_dev
#     package and publish the source distribution into your artifactory name (hosted)
#     which is also needs to be defined in your ~/.pypirc file
#
# * see also publish_minor and publish_major tasks

# run invoke --list for all task listing
# run invoke --help <task-name> for task specific docstring and arguments

# you can also run muliple commands in the same line. ex. "invoke clean install test bump_build"
# for additional info see http://docs.pyinvoke.org


@task
def commit(runner):
    """
    this will git push version related files and git tags. supporting the bump and publish functions
    """
    runner.run("git push --tags")
    runner.run("git push")


@task
def bump_build(runner):
    """
    this will bump the patch part of this module's version (major.minor.PATCH)
    """
    runner.run('bumpversion patch')
    commit(runner)


@task
def test(runner):
    """
    this will run all discovered unittests
    """
    runner.run("python -m unittest discover -v")


@task
def bump_minor(runner):
    """
    this will bump the minor part of this module's version (major.MINOR.patch)
    """
    runner.run('bumpversion minor')
    commit(runner)


@task
def bump_major(runner):
    """
    this will bump the major part of this module's version (MAJOR.minor.patch)
    """
    runner.run('bumpversion major')
    commit(runner)


def publishCommand(repo):
    additional_args = "" if not 'PYDIST_ARGS' in os.environ else os.environ['PYDIST_ARGS']
    return "python setup.py sdist upload -r {} {}".format(repo, additional_args)


@task
def publish(runner):
    """
    this will build and publish this module's source distribution file into artifact repository name indicated by the --repo parameter
    """
    additional_args = "" if not 'PYDIST_ARGS' in os.environ else os.environ['PYDIST_ARGS']
    runner.run("python setup.py sdist upload -r $ARTIFACTORY_REPO_KEY {}".format(additional_args))


@task(bump_minor, help={'repo': 'repository name. as configured in your .pypirc'})
def publish_minor(runner, repo):
    """
    this will build, bump minor then publish this module's source distribution file into artifact repository name indicated by the --repo parameter
    """
    runner.run(publishCommand(repo))


@task(bump_major, help={'repo': 'repository name. as configured in your .pypirc'})
def publish_major(runner, repo):
    """
    this will build, bump major then publish this module's source distribution file into artifact repository name indicated by the --repo parameter
    """
    runner.run(publishCommand(repo))


@task
def publish_now(runner, repo):
    """
    this will publish the current module's source distribution file without bumping version - into artifact repository name indicated by the --repo parameter
    """
    runner.run(publishCommand(repo))


@task
def clean(runner):
    """
    this will delete all run or compile produced resources
    """
    runner.run("rm -rf *.pyc")


@task
def install(runner):
    """
    this will install all required packagaes listed in requirements.txt file
    """
    runner.run("pip install -r requirements.txt")


@task
def build_image(runner):
  runner.run("docker build . -t exl_common --rm")

@task(build_image)
def run_image(runner):
  runner.run("docker run -i exl_common")

@task
def publish_image(runner):
  if (not 'GIT_TOKEN' in os.environ):
    print ("please provide your git token in GIT_TOKEN env var")

  git_token = os.environ['GIT_TOKEN']
  runner.run("docker build . --build-arg GIT_TOKEN={} -f publish.dockerfile --rm --no-cache ".format(git_token))
