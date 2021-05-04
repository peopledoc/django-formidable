==========================
Maintainers' documentation
==========================

How to release
==============

The contents of this section is a detailed version of the "release" part of the :file:`.github/PULL_REQUEST_TEMPLATE.md` file.

Requirements
------------

You can use a dedicated virtualenv, or install the following in your userspace, but these should be available in your ``$PATH``:

* Python3 (any version)
* `twine <https://pypi.org/project/twine/>`_

Pre-release
-----------

* Create a branch with an adequate name, such as ``release/x.y.z``.
* Edit the :file:`formidable/__init__.py` source file and change the value of ``formidable.version`` to the appropriate version number.
* Amend the :file:`CHANGELOG.rst` file to reflect your change. Put there the version number, the date, and do not hesitate to re-arrange its content if needed (e.g.: put sub-sections in the release notes).
* *If the version deprecates one or more feature(s)* check the docs :file:`deprecations.rst` file and change it if necessary.
* Check if you have to edit other files and change them accordingly (e.g.: README).

Commit
++++++

Once your content is ready, **commit it**:

.. code::

    git commit -am "Release x.y.z"

If you want, you can also make a more detailed commit message, by copying/pasting the contents of the Changelog.

Push
++++

**Push your branch** on Github and wait for the CI to return green.

You can also start to **create your Pull-Request** at this point, and check if you are at the correct step in the "Release" checklist.

.. attention:: When to tag?

    If you are very confident, you can tag here. But we'd recommend to wait to be sure that you have everything sorted out.

Back to development
+++++++++++++++++++

* Edit the :file:`CHANGELOG.rst` file to add a "master (unreleased)" section, with a dummy log item, such as "Nothing to see here yet".
* Edit the :file:`formidable/__init__.py` source file and put a non-release version number, such as ``x.y+1.0.dev0``.
* Commit this change with, for example, the following command: ``git commit -a -m "Back to dev => x.y+1.0.dev0"``

Again, push the branch and wait for the tests to be green.

**At this point, the pull-request should be ready for review**.

Release
-------

If the CI has returned a successful result, and your peers have reviewed your PR, you're ready to proceed with the release.

Tag the right commit
++++++++++++++++++++

You should have two commits in your log corresponding to your latest changes:

.. code:: shell

    $ git log --pretty=format:'%h %ad | %s' --date=short -n 2
    8fd30ec 2021-04-29 | Back to dev => x.y+1.0.dev0
    5b65073 2021-04-29 | Release x.y.0

Checkout to the "Release" commit and tag it.

.. code:: shell

    $ git checkout 5b65073
    $ git tag x.y.0

This tag can be pushed to Github with:

.. code:: shell

    $ git push --tags

Generate files
++++++++++++++

Now you can generate the files using the following command at the root of the project:

.. code:: shell

    $ python3 setup.py sdist bdist_wheel

This should produce two files:

* :file:`dist/django-formidable-x.y.0.tar.gz`
* :file:`dist/django_formidable-x.y.0-py3-none-any.whl`

Merge the Pull Request
++++++++++++++++++++++

Merge from Github, or, if you dislike merge commits, type the following commands from your local copy:

.. code:: shell

    $ git checkout master
    $ git merge --ff release/x.y.z
    $ git push

Upload to PyPI
++++++++++++++

In order to upload to PyPI, you should have an account and have at least the *maintainer* or *owner* role for this project **and** have your :file:`.pypirc` correctly configured to upload files (i.e. have the pypi repository as default and correct credentials, using your password or a project token).

Using ``twine`` you may now upload the two files previously generated:

.. code:: shell

    twine upload dist/django-formidable-x.y.0.tar.gz dist/django_formidable-x.y.0-py3-none-any.whl

You can then go to https://pypi.org/project/django-formidable/ to check the latest version.

.. hint::

    Due to asynchronous tasks and cache invalidation, the latest version may not appear immediately. Be patient.

Post-release
------------

There are a few cleanup tasks, such as:

* Delete the release branch,
* Edit the Release page on Github to reflect the changelog,
* Eventually make some feedback on the issues impacted by the new release,
* Enjoy & celebrate!
