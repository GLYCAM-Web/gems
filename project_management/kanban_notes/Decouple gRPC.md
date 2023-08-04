## Overview
- [ ] Move gRPC logic to networkconnections/grpc.py
- [ ] Make tests that apply only to gRPC
- [ ] Ensure that the gRPC can be relatively autonomous

BUT....
- [ ] Each gRPC connection needs to be specific.
- [ ] Make it easy for them to include testing.

## Where the Code Is
- Calls from code:  deprecated/batchcompute/slurm/receive.py
- The gRPC-native parts: gems/gRPC

## Testing
It needs to be possible to test the gRPC connection itself without executing any other code.  I suspect gRPC has built-in ways to do that, but it might not.