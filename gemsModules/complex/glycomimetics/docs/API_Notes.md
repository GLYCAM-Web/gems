MOVING THIS TO GEMS
It will be in complex/glycomimetics/doc

Early notes about designing the Glycomimetics API.  These might go stale rapidly as things evolve.

## Services

### Validate
Ensure that the inputs are complete, accessible, readable and in acceptable format.

### Evaluate
Report the options available for processing the given inputs.  At this phase, the PDB file should be evaluated.  This probably involves running pdb2glycam.

### Build Selected Positions
Builds all Libraries requested for each Position.

#### *Build Position*
*Builds all Libraries requested at this specific Position.*

##### *Build Library*
*Builds a single Library requested at this specific Position.*

### Analyze Selected Positions
Returns an over-all analysis of all Position modifications from all Libraries.

#### *Analyze Position*
*Returns an over-all analysis of all Libraries used for this Position.*

##### *Analyze Library*
*Returns an analysis of the results from this single Library at this specific Position.*


The breakdown of the Build and Analyze services was necessitated by the capabilities apparent from this image:

![[Screenshot 2024-04-15 at 11.13.51 AM.png]]

## Common GM API Objects 
These API Objects are common to one or more Inputs and/or Outputs.

### PDB File
- Might be a proper PDB file or a variant or modified PDB file

### All R Group Libraries
- List of R group libraries available for the given PDB file.

### Position Modification Options
Each containing:
- Position - a Modification Position object
	- Residue Index Number (with insertion code if needed)
	- Attachment Atom - the atom in the residue to which the mods will be attached
	- Replaced Atom - the atom in the residue that will be replaced by the mod
- Libraries 
	- Optional.  List of R-group libraries specified at this position.  
		- Evaluation:
			- If included, these are the libraries available at this position.  Must be a subset of All R Group Libraries
			- If not included, then this position can use any of the available libraries specified above.
		- Build Position
			- If not included, all available libraries will be used.
			- If included, only the specified libraries will be used


## Input 

### Validate & Evaluate
These two services have the same input (is this generally true? I think so).  An Evaluate request will always trigger a Validate request.

- PDB File
	- Location, currently: filesystem path or URL

### Build Selected Positions
This will build all the selected libraries at the selected positions.

- Default R Group Libraries - these are used if not specified in the Selected set.
- Selected Modification Options - List of Modification Options

## Output

### Validate
Either
- Inputs are valid
- Inputs are invalid with Notices as needed

### Evaluate
If Validate failed:
- Notice of failure due to dependency failure
Else:
- Default R Group Libraries - placed at the top for convenience in making a table
- Available Modification Options - a List of Modification Options.


# Below this are notes that are not directly related

## Common Resources
I'm seeing a need for the definition of common resources.  These would be resources that are used by multiple Entities and in multiple Services.  

Some might merely be common to, say, the complex module.  For example, any of the docking files are unlikely to be used elsewhere.

Others might be generally common.  PDB files are an obvious entry here.  Also system stuff like working directories.

### Truly Common
- PDB file - strict:  a PDB file in proper PDB format.
- PDB file - variant:  a PDB file that does not fully conform to proper PDB format.

### Common to Complex
- PDBQT - PDB variant used by Autodock
- Roles:
	- Ligand
	- Receptor


### Common to Conjugate
...these are more-or-less the same as Complex...  sigh.

### Common to MM Service?

The definitions of the AMBER files should probably live in mmservice/amber and not at some other level.

