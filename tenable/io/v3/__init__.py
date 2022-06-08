'''
Version3 API
============

The following sub-package allows for interaction with the Tenable.io -
Version3API

Methods available on ``tio.v3``:

.. rst-class:: hide-signature
.. autoclass:: Version3API
    :members:

.. toctree::
    :hidden:
    :glob:

    was/index
'''
from tenable.base.endpoint import APIEndpoint
from tenable.io.v3.explore import Explore


class Version3API(APIEndpoint):
    '''
    This will contain property for all resources/app under io- Web Application Security.
    '''

    @property
    def explore(self):
        '''
        The interface object for the
         :doc:`Tenable.io v3 Web Application Scanning <was/index>`
        '''
        return Explore(self._api)