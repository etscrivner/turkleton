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

Turkleton aims to leverage the expressive powers of Python to make using
Mechanical Turk easier. The highlights are:

* Simple interface to define human intelligence tasks (HITs).
* Define schemas for your results before downloading them.
* Easily upload tasks in batches.
* Easily download and validate assignments.

Examples
--------

Some basic terminology is required to get up and running with Turkleton.

A Task is a Human Intelligence Task (HIT). To get started with Turkleton you
should first create a layout for your task in Mechanical Turk. You then provide
your layout ID to turkleton as part of your task definition.

Assignments contain the answers given by a turker to the questions in your
task. An assignment defines the schema for the answers. Turkleton then uses
your assignment to parse and validate the answers it receives.

Setting Up Your Connection
^^^^^^^^^^^^^^^^^^^^^^^^^^

The first thing you need to do is setup your connection to Mechanical Turk.

Turkleton uses a per-process global connection. You should always initialize it
before you attempt to upload or download anything. You initialize it like so:

.. code-block:: python

   from turkleton import connection
   connection.setup(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

That's it!

Creating A Task And Uploading It
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you've created your layout on Mechanical Turk you can create HITs by
defining a task in Turkleton.

To define a HIT you create a Task representing the template of the
assignment you want a worker to complete. For example:

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

Now that you've defined your task you can easily upload HITs as follows:

.. code-block:: python

   task = MyTask(image_url='http://test.com/img.png', first_guess='29')
   hit = task.upload(batch_id='1234')

This will create a new assignment from the task template and upload it to
Mechanical Turk. The variables image_url and first_guess in your template will
contain the values given. The optional batch_id parameter allows you to set the
requester annotation for the task to an arbitrary string. This is useful when
you've uploaded more than one task in a batch. In the evaluation phase you can
filter which assignments are downloaded by a given batch id.

Uploading Multiple Tasks
^^^^^^^^^^^^^^^^^^^^^^^^

Usually you want to upload more than a one task. Turkleton provides two methods
for easily doing this.

The first method uses the create_and_upload method on your Task as follows:

.. code-block:: python

   for image_url in all_image_urls:
       MyTask.create_and_upload(
           image_url=image_url, first_guess='29', batch_id='1234'
       )

It is often convenient to only set the batch id once. The task.batched_upload
context manager is providing to make this approach easy as well:

.. code-block:: python

   with task.batched_upload(batch_id='1234')
       for image_url in all_image_urls:
          MyTask.create_and_upload(image_url=image_url, first_guess='29')

Every task you upload within the context will be automatically given the
specified batch id.

Downloading The Results
^^^^^^^^^^^^^^^^^^^^^^^

When you want to download your results you'll need to define an assignment. The
assignment defines the types of values you expect to get. These are used to
automatically parse and type cast your answers so you can just deal with
evaluating the results.

You can define a simple task for categorizing an image as follows:

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

Each HIT may have multiple assignments associated with it. This is the case if
the __assignments_per_hit__ attribute in your task contains a number greater
than 1.

Now that you have the HITs you can download all the assignments, review them,
and dispose of the HIT as follows:

.. code-block:: python

    for each in MyAssignment.get_by_hit_id(hit.hit_id):
        print('{} - {} - {}'.format(each.categories, each.notes, each.does_not_match_any))
        if is_valid_assignment(each):
            each.accept('Good job!')
        else:
            each.reject('Assignment does not follow instructions.')
    hit.dispose()
