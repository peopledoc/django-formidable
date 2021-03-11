=========
ChangeLog
=========

Release 7.0.0 (2021-03-11)
==========================

- Allow empty description on ``Formidable`` model

Release 6.1.0 (2020-10-07)
==========================

- Pass context to serializer in from_json.
- Fix license reference in setup.py (#402).

Release 6.0.0 (2020-10-07)
==========================

Breaking Changes
----------------

- Drop support for Python 3.5 (EOL: 2020-09-13).
- Default values for readonly fields are kept in cleaned_data.

Other changes
-------------

- Applying isort v5+ changes: no ``--recursive flag``, removed the ``not_skip`` settings. (internal change, no runtime impact).

Release 5.0.0 (2020-06-30)
==========================

Breaking Changes
----------------

- Include the property ``parameters`` when serializing a form using the ContextFormSerializer.
- Drop support for Django 1.11 (#398, #395).
- Drop support for Django REST Framework 3.8 (#382).

Other changes
-------------

- Fix Postgresql configuration in CircleCI regarding the authentication (#395).
- Small cleanups of Python2-related code.

Release 4.0.2 (2020-02-13)
==========================

- HOTFIX: Allow empty values for ``defaults`` properties (#391).

Release 4.0.1 (2020-01-21)
==========================

- DOC: removed ``setup.py`` Python2-related classifiers (#380).
- Fix the support for conditions when their trigger field is a multiple choice field (#381).

Release 4.0.0 (2020-01-08)
==========================

- Drop support for Python 2.7 -- EOL: January 1st, 2020 (#377).
- Added an XSS prevention mechanism. See the `security documentation <https://django-formidable.readthedocs.io/en/master/>`_ for more information and details on how to setup your own sanitization process (#378).
- Removed ``tox.ini`` directive that skipped missing Python interpreters (#376).

Release 3.3.0 (2019-11-29)
==========================

- Add support to Django 2.2 (#326).
- Add support to Python 3.7 & 3.8 (#374).

Release 3.2.0 (2019-11-07)
==========================

- Extend the test matrix to spread through different DRF versions.
- Drop support for Django 1.10 (EOL was in December 2nd, 2017).
- Launch tests on Postgresql as well as SQLite. Launching these tests will be possible both locally and on Circle-CI. See the "dev" documentation on how you can run tests on your development environment (#161).
- Add ``select_for_update()`` on selection in querysets when the Form is about to be modified (namely ``PUT`` & ``PATCH`` views). This could prevent Database deadlocks when several changes are attempted on the same **large** form.
- Upgrade to swagger-ui 3.23.11 (#371 & #367).

Release 3.1.0 (2019-06-03)
==========================

- Fix documentation build (#363).
- Upgrade requirements to Django REST Framework 3.9.x.

Release 3.0.1 (2019-03-01)
==========================

- Clean up help_text migration (#292)
- Freeze perf-rec version for the python 2.7

Release 3.0.0 (2018-10-31)
==========================

Main Changes
------------

- Added a plugin mechanism, allowing users to define and integrate their own "business logic" fields (#345).
- Extend the validation in the filler API to allow validation of extra fields (#348).
- Refactoring of the field builder (Use only one module for the form builder factory) (#347).
- Add `parameters` to the fields schema.
- Allow Fields and Widgets to introduce `parameters` when being stored as Formidable models instances (#358).
- Added pytz as a requirement.
- Enforce support for Django REST Framework to the version 3.8.x ; **the 3.9 series is incompatible with our current codebase**.

Minor Changes
-------------

- Upgrade to Circle-CI 2 (before the end of life of Circle-CI v1 on August, 31st 2018). (#342)
- Optimize Circle-CI usage by using the tox matrix in tests (#343)
- Change the global exception handling error level, from "error" to "exception". It'll provide better insights if you're using Logmatic or any other logging aggregator (#336).
- Skip `tox` installation in the circle-ci environment: it's already there (#344).

Release 2.1.2 (2018-08-29)
==========================

- Django field `disabled` option are now set through the field builder (#351).

Release 2.1.1 (2018-06-22)
==========================

- Moved the injection of the JSON ``version`` into the serializer, rather than the ``Formidable.to_json()`` class method. The serializer is called by the method, so it's idempotent (#340).

Release 2.1.0 (2018-06-21)
==========================

- Added the JSON ``version`` when going through the ``Formidable.to_json()`` class method. This would ensure that stored schemas would carry their version and wouldn't need extra JSON schema migrations (#337).

Release 2.0.0 (2018-05-30)
==========================

- Deprecate support for Django 1.8 and Django 1.9 (#325).
- Drop crowdin for translation handling (#333).

Release 1.7.0 (2018-04-20)
==========================

**Deprecation Warning**: Support for django<=1.9 will be dropped by the version 2.0.0.

- Added a tool to build the JSON Schema from the ``formidable.yml`` file, and include it into the documentation.
- Add a deprecation warning for django 1.8 and 1.9 (#325).

Release 1.6.0 (2018-04-06)
==========================

- Added compatibility with Python 3.6 (#318).
- Allow change type for the fields without changing name/slug

Release 1.5.2 (2018-03-30)
==========================

- Allow null and empty condition names.
- Added compatibility tests using Django 1.11.

Release 1.5.1 (2018-03-28)
==========================

- Make sure that the `ValidateView.form_valid` method return an actual empty body content along with a 204 HTTP status response. Before this hotfix, the dictionary passed along as the response content was serialized into a 2-character string to calculate the content-length, but this content was not returned to the client. Some browsers would experience it badly, namely IE11 (#313).

Release 1.5.0 (2018-03-09)
==========================

- Trim whitespaces in the generated ``formidable.js`` file. This is more than just cosmetics, it prevents to have a polluted history on this file (#306).
- Added tests to use conditional rules with drop down lists (#304)
- Added possibility to restrict types of the conditional rules (#304)
- Hotfix: Extract conditions and filter them using the fields that exist in the form (#308).
- Added typing to the demo requirements (#311)
- Make the conditional rule name optional (#307)

Release 1.4.1 (2018-03-06)
==========================

- Added Hotfix from #308: Extract conditions and filter them using the fields that exist in the form.

Release 1.4.0 (2018-02-21)
==========================

**Deprecation Warning**: The validation endpoint (using the URL ``forms/(?P<pk>\d+)/validate/``) is now ``POST`` only.

- Added tests against the ``formidable.yml`` schema definition of Forms (#295).
- Fixed various items in the schema definition (#297).
- Validation endpoint for **user data** doesn't allow GET method anymore (#300).
- Add support for multiple conditions to target a common field.

Release 1.3.1 (2018-03-06)
==========================

- Added Hotfix from #308: Extract conditions and filter them using the fields that exist in the form.

Release 1.3.0 (2018-02-14)
==========================

**Deprecation Warning**: The validation endpoint (using the URL ``forms/(?P<pk>\d+)/validate/``) was only accessible via the ``GET`` verb. It may have caused issues if we tried to validate very long forms, or forms with very large values, by hitting the querystring size limit. As a consequence, as of 1.3.0, the ``GET`` method is deprecated in favor of the ``POST`` method.

- Allow POST method for form validation endpoint.
- [Documentation] Fixed a missing ``cd`` in docs. You can't run pytest from project root (#293).
- includes 7 more languages (not translated yet): Czech, Danish, Finnish, Canadian French, Hungarian, Japanese, Swedish.

Release 1.2.2 (2018-03-06)
==========================

- Added Hotfix from #308: Extract conditions and filter them using the fields that exist in the form.

Release 1.2.1 (2018-01-12)
==========================

- Keep only existing fields ids for current role in the conditional part

Release 1.2.0 (2018-01-09)
==========================

- Allow wrong field ids in conditions

Release 1.1.0 (2017-12-04)
==========================

- Added tests for the validators mapping
- Minor syntax changes
- Added perf rec tests
- Add configuration for py.test
- Reactivate accidentally skipped ``test_validations.py`` tests
- Add JSON migrations
- ``FormidableItem.value`` field size now has no limit (``TextField``)
- Migrate to PeopleDoc GitHub organization (#283)

Release 1.0.2 (2017-10-10)
==========================

- As of its 3.7 version, it appears that Django REST Framework is no longer compatible with Django 1.8. Added a mention in the README, in the deprecation timeline, and changed tox requirements to reflect this (#272).
- Drop Preset tables (#255).

Release 1.0.1 (2017-10-04)
==========================

- Validation View return the right content-type headers when the validation is okay (#257)
- Fix The error 500 when the formidable object is not found on validation view (#257)
- Fix a 500 error with Mandatory File Fields and conditional display (#263).
- Added tests for the generic exception handler (#263).
- Added Python 3.4/3.3 support deprecation in the Deprecation Timeline documentation (#262).

Release 1.0.0 (2017-09-08)
==========================

- Drop Django REST Framework 3.3 support (#239).
- Removed the Presets from the code (#249).
  - Removed from model serializers, and test code.
  - Translation strings have been removed.
  - Swagger documentation updated to reflect this API change.
  - Removed fields that reference preset models in forms and preset args tables through a Django migration (#259).

.. warning::

    Validation rules are handled by field validations, and the historical Preset mechanism is now deprecated. Front-end integration should take into account that the form ``presets`` key is not sent to it anymore, and won't be taken into account if sent to the backend.

Release 0.15.0 (2017-08-28)
===========================

- [Doc] New Makefile target to serve the documentation.

.. warning::

    This version is the last one to support Form Presets (form validation rules). The whole software logic and data will be wiped off on the next release. If needed, make backups and try to convert your existing presets to field validation rules. refs #249.

.. warning::

    This version is the last one to support Django Rest Framework 3.3. Please upgrade to the latest available to date (3.6.2). refs #239.

Release 0.14.0 (2017-08-23)
===========================

- Add a ValidateView that works with ContextForm JSON (#246).

Release 0.13.1 (2017-07-17)
===========================

- Fix field builder from schema for Title and Separator (#243).

Release 0.13.0 (2017-07-13)
===========================

- Add contextualize function for form definition (#241).
- Small flake8-related fixes (#240).

Release 0.12.0 (2017-07-04)
===========================

- Moving file named `LICENCE` into `LICENSE` (#232).
- Add JSON schema migration (#234)
- Add a tool to convert ContextForms to FormidableJSON (#236)
- Drop python3.4 support (#234)
- Add conditional display-iff (#198).
- Added latest translations from Crowdin.

Release 0.11.1 (2017-05-19)
===========================

- Make trailing slash not mandatory for the API (#75)

Release 0.11.0 (2017-05-10)
===========================

- Added a tox job to update/refresh the swagger-ui related static files (#210 / #213) - including documentation for developers.
- Remove the field size limit for the model field `formidable.models.Item.label` (#225).
- Handle decimal values in Number fields (#227).

Release 0.10.0 (2017-04-28)
===========================

- Change errors format returned in the builder in order to have something
  more constistant (#214)
- Add input_type to format field (help_text, separator, title) (#218)

Release 0.9.1 (2017-04-24)
==========================

- Use an atomic transaction in FormidableSerialize.save() (#220)
- Ensure compatibility with Django REST Framework 3.3 (#222)

Release 0.9.0 (2017-04-11)
==========================

* Added Django 1.10 support (#203).
* Dropped Python 3.3 support (#207).
* Fixed the swagger doc generation and rendering (#210).
* Fix wrong field type for Checkbox (#208).
* Don't rely on database ordering in `NestedListSerializer` (#215)
* Provide a tools in order to generate django-form class from json
  contextualized definition (#171)

Release 0.8.2 (2017-03-28)
==========================

* Enforce unicity of keys in NestedListSerializers (#202)
* Define __unicode__ and __str__ on models (#200)
* Fix regression on presets_lists endpoint (#199)

Release 0.8.1 (2017-03-07)
==========================

- Fix: Serializers don't allow empty (blank) description on Field and Item (#194).

Release 0.8.0 (2017-03-06)
==========================

* [ci] Split tox jobs into CircleCI configuration (#189).
* Skip form validation rules if a field is empty (#191).
* Fix: Confirmation preset validation would correctly compare using the appropriate types (#177).
* Change `help_text` to `description` in the API, in order to catch up formidable-ui (#188).

Release 0.7.1 (2017-02-22)
==========================

* Fix: excluding the `.crowdin` directory in the flake8 tox job (#179).
* Return the preview mode (form or table) with the accesses list (#121)
* Fix: avoid installing formidable when not needed in tests - flake8 + isort checks (#181).
* add presets to ContextFormSerializer (#176). Add presets creation directly in a FormidableForm declaration. Rework tests with presets.
* Fix: error message for preset validation is not the one specified (#185)
* Improve isort management in tox file (#147)

Release 0.7.0 (2017-02-15)
==========================

* Renamed exception class for unknown access (#166)
* Added str() methods to models (#167)
* Added ``build/`` and ``dist/`` directories to ``.gitignore`` (#174)
* Added crowdin support and updated translations for presets ; added a first round of French translation for demonstration purposes (#168)

Release 0.6.0 (2017-01-17)
==========================

* Added a make target to install the demo site (#152).
* Added django-perf-rec module for tests and improved SQL queries in `ContextFormDetailView` (#54, #154, #160).
* Added test to count queries on dynamic form queryset + improve performances (#155, #156, #162).
* Added test to count queries on retrieve builder view + improve performances by removing duplicate queries (#157, #158, #163).


Release 0.5.0 (2017-01-10)
==========================

* Fix the demo site to work with Django 1.8 *and* with logged-in users (#146).
* Added a callback on success / failure mechanism (#134).


Release 0.4.0 (2017-04-01)
==========================

* Fix the validation view with mandatory file (#140)
* A few typo fixes in documentation (#128).
* Added a Makefile autodocumentation (#127).
* Added a tox target to build documentation (#130).
* Fix autodoc generation (#131).
* Added flake8 checks via tox (#133).
* Added tox posargs to pass extra arguments when running tests (#135).
* Solve ``setup.py install`` "zip" error. Skip global package installation (#139).
* Moving ``check-python-imports`` test to the tox file (#138).

Release 0.3.1 (2016-11-04)
==========================

* Can override the way to get the formidable object in the validation view.


Release 0.3.0 (2016-10-11)
==========================

* Can add custom permission to custom view

Release 0.2.2 (2016-08-25)
==========================

* Fix the generation of checkboxes field (#115)


Release 0.2.1 (2016-08-19)
==========================

* Fix name URL's form_detail has been rename to form_context


Release 0.2.0 (2016-07-21)
==========================

* Cleans up python method (#111)
* Add dummy edition mode on python builder (#109)
* Enable custom permission on API view (#105)
* Add email Field (#100)


Release 0.1.1 (2016-07-07)
==========================

* Do not set the "disabled" attribute in "input" type when it's not needed. (#103)

Release 0.1.0 (2016-06-29)
==========================

* Define constants for access right 2 - Working <= 5 enhancement (#88)
* Disabled field don't send data on submit! bug question (#79)
* Turn defaults value into a list of strings refactor (#77)
* Rename value to label for fields items refactor (#76)
* Ordre des items dans les fields à choix. (#69)
* Define ``FileField`` in FieldBuilder (pure Django) (#68)
* Fix radiobutton type ID through JS builder (#67)
* Python 3/2 compatibility (#66)
* Fix multiple choices in the final Django Form class (#63)
* Fix the order field creation and rendering in data serialization (#61)
* Add validation Presets (#60)
* Rename "helpText" to "help_text" (#57)
* Add docs (#53)
* Implement TitleField/SeperateField/HelpTextField (#51)
* Add contextualized serializer tests (#49)
* Add date choice (#45)
* Add the form context serializer (#44)
* Add validation on field object (#41)
* Handle order of fields on save (#37)
* Fix the creation and edition of nested fields in form serializer (#35)
* Make real object for access (#32)
* Add ID field for the form object serialized (#31)
* Django Form from an Formidable object (#29)
* Ember Integration for demo project (#28)
* Tests for API REST calls (#27)
* Control level access and constants (#22)
* Refactor of the generic listserializer (#20)
* Add the update view forgotten (#18)
* Field Validation (#16)
* Implementate role accesses (#14)
* Update 3-level forms (#10)
* Add create via API (#8)
* Implement a fieldserializer for each type of fields (#6)
* Add README and Makefile (#5)
* Setup CI for the API (#4)
* Add python Builder (#3)
* Use Django Rest Framework for the API (#2)
* Bootstrap django-formidable (#1)

Developers
----------

* Guillaume Camera <guillaume.camera@people-doc.com>
* Guillaume Gérard <guillaume.gerard@people-doc.com>
