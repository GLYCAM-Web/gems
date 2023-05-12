## Services

Today:  Design UX for Run_MD

- [ ] netcdf to ascii  - for WinX users, make possible to get an ascii version on demand
- [ ] evaluation step  - there should, for sure, be an evaluation step (how long will it take, etc)
- [ ] go to 11  - the 10 Dan Roe steps will always happen, with the minimal MD production.  If someone requests fee-for-service MD, then there will be an 11th step (or more)
- [ ] allow nc as input is v2  - we will eventually need.  Don't code us out of this.
- [ ] make suggested input  - design the UX & ask for feedback.  By end of week.
- [ ] just single step at first to prove flow - get into the live sites ASAP,  single step is fine, just to prove flow

Later: Query

Later:  All the defaults (Marco, etc.)

## Tasks

### RunMD

This first version is going to be an enormous hack.  Apologies in advance to whoever needs to clean up after me.

All of this code exists in some way or another.   I just need to hack it together for this very specific purpose.

- [x] Assign working directory naming needs to happen higher up
- [x] Ensure that the input files exist in the expected location
- [x] Generate an output (working) directory
- [x] Copy the input files to the output directory
- [x] Copy the MD files to the output directory
- [x] Have the amber entity do what it needs to do
- [x] I think the following part needs to be a daemon>
	- [x] Have batchcompute and/or batchcompute/slurm generate input files
	- [x] I think the submission happens automatically
- [x] Collect and send back the response

