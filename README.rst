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

Installation
------------

Simply use pip to download the package from PyPI

.. code-block:: shell

   $ pip install turkleton

Features
--------

The existing Python APIs for Mechanical Turk are thin wrappers at best - we can
do better.

Turkleton aims to leverage the expressive powers of Python to improve the whole
situation. While still under active development, the main features are:

* Simple interface for defining tasks from pre-built layouts.
* Simple interface for defining schema of assignment results.
* Easily upload tasks in batches.
* Easily download and validate assignments.

Examples
--------

In turkleton there are several objects to be aware of: Tasks, HITs, and
Assignments. A Task is a template from which HITs are created. A HIT
corresponds to HIT in the Amazon Mechanical Turk API and represents an uploaded
Task. Assignments are contained within HITs. An individual Assignment
represents the set of answers submitted by a single worker. A HIT can have many
Assignments.

Setting Up Your Connection
^^^^^^^^^^^^^^^^^^^^^^^^^^

Turkleton uses a per-process global connection. It should be initialized before
you attempt to upload or download anything. You can initialize it like so:

.. code-block:: python

   from turkleton import connection
   connection.setup(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

That's it!

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
       __keywords__ = ['image', 'categorization']
       __time_per_assignment__ = datetime.timedelta(minutes=5)

Here we've created a Task from an existing layout. Now that we've defined our
task we can easily upload HITs by filling out the layout parameters:

.. code-block:: python

   task = MyTask(image_url='http://test.com/img.png', first_guess='29')
   hit = task.upload(batch_id='1234')

This will create a new assignment from the task template and upload it to
Mechanical Turk. The optional batch_id parameter allows you to set the
annotation for the task to an arbitrary string that you can use to retrieve
tasks later in batches.

You can upload many tasks in a loop easily as follows:

.. code-block:: python

   for image_url in all_image_urls:
       MyTask.create_and_upload(
           image_url=image_url, first_guess='29', batch_id='1234'
       )

If you'd like to leave off the batch id you can also use the context manager:

.. code-block:: python

   with task.batched_upload(batch_id='1234')
       for image_url in all_image_urls:
          MyTask.create_and_upload(image_url=image_url, first_guess='29')

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
        notes = answers.TextAnswer(question_name='AdditionalNotes', default='')
        does_not_match_any = answers.BooleanAnswer(
            question_name='DoesNotMatchAnyCategories', default=False
        )

You can then download all of the HITs in a given batch as follows:

.. code-block:: python

    from turkleton.assignment import hit
    reviewable_hits = hit.get_reviewable_by_batch_id('1234')

Each HIT may then have multiple assignments associated with it. You can
download the assignments, review them, and then dispose of the HIT as follows:

.. code-block:: python

    for each in MyAssignment.get_by_hit_id(hit.hit_id):
        print('{} - {} - {}'.format(each.categories, each.notes, each.does_not_match_any))
        if is_valid_assignment(each):
            each.accept('Good job!')
        else:
            each.reject('Assignment does not follow instructions.')
    hit.dispose()
