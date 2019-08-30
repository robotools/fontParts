.. highlight:: python

######################
Implementing FontParts
######################

The whole point of FontParts is to present a common API to scripters. So, obviously, the way to implement it is to develop an API that is compliant with the :ref:`object documentation <fontparts-objects>`. That's going to be a non-trivial amount of work, so we offer a less laborious alternative: we provide a set of :ref:`base objects <implementing-subclassing>` that can be subclassed and privately mapped to an environment's native API. If you don't want to use these base objects, you can implement the API all on your own. You just have to make sure that your implementation is compatible.


.. toctree::
    :maxdepth: 2
    :includehidden:

    testing/index
    objects/index
    layers/index
