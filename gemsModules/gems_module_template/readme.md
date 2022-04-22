Use this module to save time setting up a new gems module.

Copy this dir into a new one and give that the same name as your entity.
Then you will need to edit the following:
- helpme.md
- readme.md
- settings.py
- receive.py

From there, you will need to:
- register your new gems module with the common gems module settings.py
- register your services in common/transaction.py
- define your data models in a new file you will create, named io.py
- validate incoming requests against those models via pydantic
- create new python scripts (modules) for each service you need
- delegate to those services in receive.py, based on entity/service match
- provide a default service (usually evaluate) if no service is in request
- write tests for your services
- write documentation