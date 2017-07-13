=========
ChangeLog
=========

master (unreleased)
===================

- Nothing yet.

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
