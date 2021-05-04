## Review

This PR closes #<!-- issue number -->

* [ ] Tests<!-- mandatory -->
* [ ] Docs/comments
  * [ ] *IN CASE YOU'VE CHANGED THE `formidable.yml` file*: run ``tox -e swagger-statics`` to rebuild the swagger static files **and** commit the diff.
* [ ] Migration(s)
* [ ] `CHANGELOG.rst` Updated
* [ ] Delete your branch

<!-- THE FOLLOWING IS ONLY FOR A RELEASE PULL-REQUEST -->
<!-- uncomment the block to make it real

## Release

* [ ] Change `formidable.version` with the appropriate tag
* [ ] Amend `CHANGELOG.rst` (check the release date)
* [ ] *If the version deprecates one or more feature(s)* check the docs `deprecations.rst` file and change it if necessary.
* [ ] Commit this as "Release x.y.z"
* [ ] Push this commit and wait for CI to be green
* [ ] Tag the appropriate commit with the appropriate tag (i.e. not the "back to dev one")
* [ ] DON'T FORGET TO MAKE THE "BACK TO DEV COMMIT"
* [ ] Your PR should be ready at this stage, wait for complete review.

**Once the PR is reviewed**

* [ ] Merge using Github or `git checkout master && git merge --ff my-release-branch` (fast forward is nice, even if not required)
* [ ] Push the tag (using: `git push --tags`)
* [ ] Edit the release (copy/paste CHANGELOG)
* [ ] Generate the release files **using the tagged commit**
* [ ] Publish the new release to PyPI using `twine upload`
* [ ] Delete the release branch
-->
