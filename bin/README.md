# Compile Hooks

* [Python buildpack source][python-buildpack-source]
* [Buildpack API docs][buildpack-api]

## `pre_compile`
Unused

## `post_compile`
Runs migrations after slug compilation. If migrations fail to run, the push
will be rejected.

[python-buildpack-source]: https://github.com/heroku/heroku-buildpack-python/tree/master/bin/steps/hooks
[buildpack-api]: https://devcenter.heroku.com/articles/buildpack-api
