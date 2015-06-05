===============================
turkleton
===============================

.. image:: https://img.shields.io/travis/etscrivner/turkleton.svg
        :target: https://travis-ci.org/etscrivner/turkleton

.. image:: https://coveralls.io/repos/etscrivner/turkleton/badge.svg?branch=master
  :target: https://coveralls.io/r/etscrivner/turkleton?branch=master


.. image:: https://img.shields.io/pypi/v/turkleton.svg
        :target: https://pypi.python.org/pypi/turkleton

.. image:: https://readthedocs.org/projects/turkleton/badge/?version=latest
   :target: https://readthedocs.org/projects/turkleton/?badge=latest
   :alt: Documentation Status

Dead simple Python interfaces for Amazon Mechanical Turk.

* Free software: BSD license
* Documentation: https://turkleton.readthedocs.org.

Features
--------

The presently existing APIs for Amazon Mechanical Turk require faaaar too much
for you to get up and running. This API aims to simplify the whole process:

* Interfaces for uploading assignments from pre-built layouts.
* ORM-like interface for downloading and evaluating assignment results.

Examples
--------

In turkleton there are several objects to be aware of: Tasks, HITs, and
Assignments. A Task is a template from which HITs are created. A HIT
corresponds to HIT in the Amazon Mechanical Turk API and represents an uploaded
Task. Assignments are contained within HITs. An individual Assignment
represents the set of answers submitted by a single worker. A HIT can have many
Assignments.

Creating A Task And Uploading It
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a HIT you create a Task representing the template of the assignment
you want a worker to complete. For example:

.. code-block:: python

   import datetime

   from turkleton.assignment import task
   
   class MyTask(task.BaseTask):

       __layout_id__ = 'MY LAYOUT ID'
       __reward__ = 0.25
       __title__ = 'Guess How Old From Picture'
       __description__ = 'Look at a picture and guess how old the person is.'
       __time_per_assignment__ = datetime.timedelta(minutes=5)


Here we've created a Task from an existing layout. Now that we've defined our
task we can easily upload HITs using it to Mechanical Turk:

.. code-block:: python

   from turkleton import connection

   conn = connection.make_connection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
   task = MyTask({'image_url': 'http://test.com/img.png', 'first_guess': '29'})
   hit = task.upload(conn, batch_id='1234')

This will create a new assignment from the task template and upload it to
Mechanical Turk. The optional batch_id parameter allows you to set the
annotation for the task to an arbitrary string that you can use to retrieve
tasks later in batches.

Downloading The Results
^^^^^^^^^^^^^^^^^^^^^^^

To download results for a HIT you first need to define an assignment. The
assignment defines what values are expected and their types. These are used to
automatically parse answers to the various questions:

.. code-block:: python

    from turkleton.assignment import assignment
    from turkleton.assignment import answers
    
    class MyAssignment(assignment.BaseAssignment):
        categories = answers.MultiChoiceAnswer(question_name='Categories')
        notes = answers.TextAnswer(question_name='AdditionalNotes')
        does_not_match_any = answers.BooleanAnswer(question_name='DoesNotMatchAnyCategories')

You can then download all of the HITs in a given batch as follows:

.. code-block:: python

    from turkleton.assignment import hit
    reviewable_hits = hit.get_reviewable_by_batch_id(mturk_connection, '1234')

Each HIT may then have multiple assignments associated with it. You can
download the assignments, review them, and then dispose of the HIT as follows:

.. code-block:: python

    for each in MyAssignment.get_by_hit_id(mturk_connection, hit.hit_id):
        print('{} - {} - {}'.format(each.categories, each.notes, each.does_not_match_any))
        if each.is_valid():
            each.accept('Good job!')
        else:
            each.reject('Assignment does not follow instructions.')
    hit.dispose(mturk_connection)
