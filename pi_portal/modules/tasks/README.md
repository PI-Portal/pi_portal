# Task Scheduler Overview

In order to manage events like the power going out, or the internet going down, pi_portal uses a persistent queue to back a task scheduling system.

This is essentially an event driven system where the different components of pi_portal can communicate with each other over a robust message bus.

![overview](./markdown/task_scheduler_overview.svg)

## Components

### Tasks

Tasks are a collection of [fields](./task/bases/task_fields.py) that describe a unit work that the system needs done.

Tasks themselves are subclasses of [TaskBase](./task/bases/task_base.py) and are generated using the [MetaTask](./task/metaclasses/meta_task.py) metaclass.  The metaclass provides a mechanism to correctly type the arguments and return values of each type of task.

Tasks must be [registered](./registration/registry.py) in order to be used by the task scheduler, and should have their own module in the [task](./task) folder, with a generated test.

### Processors

Tasks themselves are just a collection of metadata describing work that needs to be done.  The actual work is done by implementations of [ProcessorBase](./processor/bases/processor_base.py)

Each task should have a corresponding processor module in the [processor](./processor) folder.

### Queues

Tasks are "scheduled" by being sent to one of the persistent queues, which are implementations of [QueueBase](./queue/bases/queue_base.py).  The implementations chosen should be hardy against abrupt system restarts and be disk based as to not rely on a network connection.  This allows the system to "resume" state in the event of a service outage.

### Routers

Tasks have a [routing label](./enums.py) property that allows them to be routed by an implementation of [RouterBase](./queue/bases/router_base.py).  The router will send each task to the correct queue for it's configured routing label.

Each [task type](./enums.py) has a [default routing label](./config.py) which can optionally be overridden during creation.

### Workers

The queue associated with each routing label will have one or more implementations of [WorkerBase](./workers/bases/worker_base.py) consuming tasks from the queue and instantiating processors to do the actual task work.  

There is also a separate [WorkerBase](./workers/bases/worker_base.py) implementation that runs a set of [cron jobs](./workers/cron_jobs) at specific intervals of time.  This worker does no task processing, but rather creates tasks to send to the queues for processing.

Finally, a third [WorkerBase](./workers/bases/worker_base.py) implementation receives failed tasks and stores them in a persistent task manifest.  These tasks are reintroduced periodically via the task router to re-attempt processing.

### Manifests

Tasks can also be stored in "manifests", which are implementations of [TaskManifestBase](./manifest/bases/task_manifest_base.py).  These are essentially persistent Python dictionaries.  

The implementations chosen should be hardy against abrupt system restarts and be disk based as to not rely on a network connection.  This allows the manifest to "resume" it's state in the event of a service outage.

### Scheduler

Managing the interaction of all these pieces is the [Scheduler](./scheduler.py) which instantiates the registry, the router (and it's queues) and then launches a set of workers according to its [configuration](./config.py).  

The scheduler is the heart of the task scheduling system.

### API

There is also an [API](./api) exposed over a Unix socket (with tightened permissions) to allow external processes that are managed by pi_portal to schedule tasks.
