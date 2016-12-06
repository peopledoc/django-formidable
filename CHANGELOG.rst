=========
ChangeLog
=========

Release 0.4.0dev (unreleased)
============================

* A few typo fixes in documentation (#128).
* Added a Makefile autodocumentation (#127).
* Added a tox target to build documentation (#130).

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
