from zope.interface import (
    Interface,
    Attribute,
    )

#
# pyramid_workflow APIs
#
class IWorkflow(Interface):
    """Finite state machine.

    Implements `pyramid_workflow.interfaces.IWorkflow`.

    :param state_attr: attribute name where a given object's current state
                       will be stored (object is responsible for persisting)
    :type state_attr: string

    :param initial_state: Initial state of the workflow assigned to the content
    :type initial_state: string

    :param type: Identifier to separate multiple workflows on same content.
    :type type: string

    :param name: Display name.
    :type name: string

    :param description: Not used internally, provided as help text to describe
                        what workflow does.
    :type description: string
    """

    def add_state(name, callback=None, **kw):
        """Add a new workflow state.

        :param state_name: Unique name of the state for this workflow.
        :param callback: Will be called when content enters this state.
                         Meaning :meth:`Workflow.reset`,
                         :meth:`Workflow.initialize`,
                         :meth:`Workflow.transition` and
                         :meth:`Workflow.transition_to_state` will trigger
                         callback if entering this state.
        :type callback: callable
        :param \*\*kw: Metadata assigned to this state.

        :raises: :exc:`WorkflowError` if state already exists.

        Callback is called with **content** as a single positional argument and
        the keyword arguments  **workflow**, **transition**, and **request**. Be
        aware that methods as :meth:`Workflow.initialize` pass **transition**
        as an empty dictionary.

        .. note::
            ``**kw`` must not contain the key
            ``callback``. This name is reserved for internal use.
        """

    def add_transition(name, from_state, to_state, callback=None, **kw):
        """Add a new workflow transition.

        :param transition_name: Unique name of transition for this workflow.
        :param callback: Will be called when transition is executed.
                         Meaning :meth:`Workflow.transition` and
                         :meth:`Workflow.transition_to_state` will trigger
                         callback if this transition is executed.
        :type callback: callable
        :param \*\*kw: Metadata assigned to this transition.

        :raises: :exc:`WorkflowError` if transition already exists.
        :raises: :exc:`WorkflowError` if from_state or to_state don't exist.

        Callback is called with **content** as a single positional argument and
        the keyword arguments  **workflow**, **transition**, and **request**.

        .. note::
            ``**kw`` must not contain any of the keys ``from_state``, ``name``,
            ``to_state``, or ``callback``; these are reserved for internal use.

        """

    def check():
        """Check the consistency of the workflow state machine.

        :raises: :exc:`WorkflowError` if workflow is inconsistent.

        """

    def state_of(content):
        """Return the current state of the content object or None
        if the content object does not have this workflow.
        """

    def has_state(content):
        """Return True if the content has state for this workflow,
        False if not.
        """

    def get_states(content, request, from_state=None):
        """Return all states for the workflow.

        :param content: Object to be operated on
        :param request: `pyramid.request.Request` instance
        :param from_state: State of the content. If None,
                           :meth:`Workflow.state_of` will be used on
                           **content**.

        :rtype: list of dicts
        :returns: Where dictionary contains information about the transition,
                  such as **title**, **initial**, **current**,
                  **transitions** and **data**. **transitions** is return value
                  of :meth:`Workflow.get_transitions` call for current state.
                  **data** is a dictionary containing at least **callback**.

        .. note::
            States that fail `has_permission` check for their transition
            are left out.

        """

    def initialize(content, request=None):
        """Initialize the content object to the initial state of this workflow.

        :param content: Object to be operated on
        :param request: `pyramid.request.Request` instance
        :returns: (initial_state, msg)

        `msg` is a string returned by the state `callback`.

        """

    def reset(content, request=None):
        """Reset the content workflow by calling the callback of
        it's current state and setting its state attr.

        If content has no current state, it will be initialized
        for this workflow (see initialize).

        `msg` is a string returned by the state callback.

        :param content: Object to be operated on
        :param request: `pyramid.request.Request` instance
        :returns: (state, msg)

        """

    def transition(content, request, transition_name):
        """Execute a transition using a **transition_name** on **content**.

        :param content: Object to be operated on.
        :param request: `pyramid.request.Request` instance
        :param transition_name: Name of transition to execute.

        :raises: :exc:`WorkflowError` if no transition is found
        :raises: :exc:`WorkflowError` if transition doesn't pass
                                      `has_permission` check
        """

    def transition_to_state(content, request, to_state,
                            skip_same=True):
        """Execute a transition to another state using a state name
        (**to_state**). All possible transitions towards **to_state**
        will be tried until one if found that passes without exception.

        :param content: Object to be operated on.
        :param request: `pyramid.request.Request` instance
        :param to_state: State to transition to.
        :param skip_same: If True and the **to_state** is the same as
                          the content state, no transition is issued.

        :raises: :exc:`WorkflowError` if no transition is found

        """

    def get_transitions(content, request, from_state=None):
        """Get all transitions from the content state.

        :param content: Object to be operated on.
        :param request: `pyramid.request.Request` instance
        :param from_state: Name of the state to retrieve transitions. If None,
                           :meth:`Workflow.state_of` will be used on
                           **content**.
        :rtype: list of dicts
        :returns: Where dictionary contains information about the transition,
                  such as **from_state**, **to_state**, **callback**,
                  **permission** and **name**.

        .. note::
            Transitions that fail `has_permission` check are left out.

        """

class IDefaultWorkflow(Interface):
    """ Marker interface used internally for workflows that aren't
    associated with a particular content type"""
