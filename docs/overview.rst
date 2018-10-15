========
Overview
========

Pangea is a platform for genomic analysis and warehousing.

Components
==========

1. :ref:`user-service` - responsible for Users, Organizations, and membership thereof
2. :ref:`sample-organization-service` - responsible for Samples, Sample Libraries, and Sample Groups
3. :ref:`tensoranalysis-service` - responsible for execution of HoloQL requests
4. :ref:`holoql-plugin` - responsible for execution of HoloQL requests
5. :ref:`worker-wrangler-service` - responsible for provisioning worker instances
6. :ref:`result-tracking-service` - responsible for monitoring long running tasks
7. :ref:`logging-service` - responsible for aggregating microservice logs and reporting errors


.. _user-service:

User Service
------------

Manages all things user- and organization-related. This includes creation, membership management, fetching of profiles, etc.


.. _sample-organization-service:

Sample Organization Service
---------------------------

Manages creation of samples, sample libraries, sample groups, and authorization of each of these.


.. _tensoranalysis-service:

TensorAnalysis Service
----------------------

This service is responsible for execution of HoloQL requests.

It defines two primary REST endpoints. The first returns a manifest describing what query elements are supported by the current instance. The second accepts a HoloQL request and executes that request.

The functionality of TensorAnalysis is extended by installation of :ref:`holoql-plugin` packages, automatically discovered at runtime. Each plugin package adds additional HoloQL methods.


.. _holoql-plugin:

HoloQL Plug-in
--------------

Plugins extending the functionality of the :ref:`tensoranalysis-service`. These can cover a wide range of functionality: external data warehouse import, HPC tasks, secondary genomic analysis, PDF generation, and more.

Modules define:

* Unique identifier *(required)* - unique name for the plug-in
* Module configuration options *(optional)* - ex. AWS S3 credentials for uploading result file
* Result storage scheme *(optional)* - defines how the results from methods will be stored:
   * Discarded -- implicit if the return value is None
   * Stored in Redis cache -- usually used for easily re-run tasks
   * Stored to database -- usually used for results from long running HPC tasks that will change infrequently
* HoloQL Methods *(optional)* - Methods to expose in this Pangea instance's HoloQL manifest. These methods generally fall into one of three categories:
   * Data suppliers - these methods take either no arguments or static arguments (e.g. a file) and return data (usually used for HPC tasks)
   * Transformer - these methods accept data as an input and return other data
   * Operation - these methods accept data and perform work without returning additional data (ex. PDF generation)


.. _worker-wrangler-service:

Worker Wrangler Service
-----------------------

*Codename: Ruth Roach*

.. After champion rodeo performer
.. other ideas: Stoney Burke, Slim Pickens, Monte Hale

The worker wrangler is responsible for minimizing compute and bandwidth costs. Worker instances are expensive to keep running but downloading all the necessary files to run HPC tasks can also be quite expensive. Worker instance types may also be quite specialized, requiring different underlying Docker images and/or provisioning steps.

The worker wrangler keeps an eye on the task queue and spins up machines when it makes sense to. It monitors spot instance pricing and makes bids appropriate for the job type. For example, a low priority job need not be completed immediately and should thus place a lower bid. Conversely, a high priority job would warrant a higher spot pricing bid. Long running HPC jobs that cannot be resumed if interrupted may require renting at the on-demand price to ensure completion of the job.

.. _pipeline-conductor-service:

Pipeline Conductor Service
--------------------------

*Codename: Beethoven*

The job reporting service provides status updates on HPC jobs (similar to the Celery Flower project).

.. _result-tracking-service:

Result Tracking Service
-----------------------

*Codename: Shadow Wolf*

.. after a DHS unit of Native American trackers

The job reporting service provides status updates on HPC jobs (similar to the Celery Flower project).

.. _logging-service:

Logging Service
---------------

*Codename: Ron Burgundy*

.. other ideas: Anchorman, Channel Four News

Aggregates logs from other microservices and reports errors.
