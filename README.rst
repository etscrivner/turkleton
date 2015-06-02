===============================
turkleton
===============================

.. image:: https://img.shields.io/travis/etscrivner/turkleton.svg
        :target: https://travis-ci.org/etscrivner/turkleton

.. image:: https://img.shields.io/pypi/v/turkleton.svg
        :target: https://pypi.python.org/pypi/turkleton


Simplified interfaces for assignments on Mechanical Turk.

* Free software: BSD license
* Documentation: https://turkleton.readthedocs.org.

Features
--------

* Interfaces for uploading assignments from pre-built layouts.
* ORM-like interface for downloading and evaluating assignment results.

Examples
--------

Here's how you would define a task template to be uploaded:

.. code-block:: python

   from turkleton.assignment import task
   
   class MyTask(task.BaseTask):

       __layout_id__ = 'MY LAYOUT ID'
       __reward__ = 0.25
       __title__ = 'Guess How Old From Picture'
       __description__ = 'Look at a picture and guess how old the person is.'


Now that we've defined our assignment we can easily upload it to Mechanical
Turk:

.. code-block:: python

   from turkleton import connection

   conn = connection.make_connection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
   task = MyTask({'param1': 'val1', 'param2': 'val2'})
   hit = task.upload(conn, batch_id='1234')

This will create a new task and upload it to Mechanical Turk. The optional
batch_id parameter allows you to set the annotation for the task to an
arbitrary string that you can use to retrieve tasks later in batches.
