# Keeping the code clean

One of the things that makes GEMS so difficult is that what users want to 
do doesn't necessarily make for clean programming. 

For example, consider this:

    class SequenceInputs(BaseModel):
        sequence: TheSequence = None
        sequenceVariants: TheSequenceVariants = None
        systemSolvationOptions: TheSystemSolvationOptions = None
        geometryOptions: TheGeometryOptions = None
        buildOptions: TheBuildOptions = None
        evaluationOptions: TheEvaluationOptions = None
        drawOptions: TheDrawOptions = None

That arrangement is convenient for users because they can just enter a 
simple list with everything they want to do.

But it also means that either:

- Every Service offered by Sequence gets a copy of this, and pretty much 
  everything else, or
- Some code must take all the information out of the various structures 
  like this one (think project info, session UUIDs, etc.) and organize them 
  into packets of only what each service needs.

For the first go-round, I decided on the first option.  That's the main reason 
why the whole Transaction got passed everywhere.  That allowed each service to 
go read whatever it needed to know.  The second option can make the code 
cleaner and easier, but it generates a maintenance burden in that something 
other than each service is required to know what each service needs and what 
each service returns.  

I am moving toward the second option, and so.... the Main Servicer is born.  It 
will be the Main Servicer's job to know all about the services, including order 
of ops, dependencies, inputs and outputs.  I hope to somehow stuff all that into
settings files for each service.  I think I can do it.  