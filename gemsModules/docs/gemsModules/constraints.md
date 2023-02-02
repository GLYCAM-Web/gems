# Constraints

These are constraints that we either need to work within or find that working
within them is desirable.

##  The API Contract

Our basic API contract is very simple, on purpose.  This is a contract that 
we can easilyt keep.

1.  The user sends a JSON object to the delegator, usually via STDIN.
2.  The delegator sends a JSON object back, usually via STDOUT.

##  The JSON Schema

Changing JSON schema is a pain for everyone.  We should not change it.  We
can add to it, but not change it.  This is the Open-Closed principle.

##  User Sanity

We must ensure that the users do not feel crazy stress when interacting with
our code or when using the JSON API.

##  New Coders

This is a teaching lab, and many of the students are not here to study 
programming.  So, the code needs to be easy for them to use.
