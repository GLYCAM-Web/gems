# Design Documentation for the Common gemsModule

This module provides infrastructure and templates for all the other modules. It is not designed to ever be
an Entity on its own, and it should almost never answer any requests itself. 

This Module has no parent Module but is a parent to most other Modules. 

## Responses from the Common Entity

A response from the 'Common Servicer' should always indicate that something has gone horribly wrong. That
is, any infrastructure for replies should make it plain that the reply is not the expected behavior, and
should only happen if all other avenues for reply are exhausted.

---

## Purpose and Goals

This Module should provide infrastructure that is common to most modules. Some infrastructure can be used
'AS IS' by the other Modules. There should be a simple and convenient way for the infrastructure to be 
adapted to the Child Module. For example, the response to the Marco Service from the Delegator Entity should
declare itself to come from the Delegator Entity and not from Common.



