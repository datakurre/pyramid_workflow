pyramid_workflow
================

.. image:: https://secure.travis-ci.org/datakurre/pyramid_workflow.png
   :target: http://travis-ci.org/datakurre/pyramid_workflow

This package is a shameless derivate of ``substanced.workflow`` module without
``substanced`` dependencies (besides its LICENSE, of course).

Differences from ``substanced.workflow``:

- workflow requires ``state_attr`` as its first positional argument
  similarly to the original ``repoze.workflow`` (and because of that
  parallel workflows should use different ``state_attr``)

- content-type related checks are removed, because there's no more
  global content registry (``substanced.content``).

Example of use:

.. code:: python

   from pyramid_workflow import Workflow

   task_workflow = Workflow(state_attr='worker_state',
                            initial_state='new',
                            type='worker')

   task_workflow.add_state('new')
   task_workflow.add_state('working')
   task_workflow.add_state('done')

   task_workflow.add_transition('start',
                                from_state='new',
                                to_state='working')
   task_workflow.add_transition('complete',
                                from_state='working',
                                to_state='done')
   task_workflow.add_transition('abort',
                                from_state='working',
                                to_state='new')

   def includeme(config):
       config.add_workflow(task_workflow, content_types=('my_type',))

See also: http://substanced.readthedocs.org/en/latest/workflows.html
