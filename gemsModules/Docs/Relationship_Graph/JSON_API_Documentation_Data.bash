#!/bin/bash

## File JSON_API_Documentation_Data.bash
## Begun on 2019-02-28 by BLFoley
## 
## Contains a concise representation of the JSON API.
##
## Is used by other scripts in this directory
## 
## Please build newer versions of the API schema from
## these scripts - or from other, better scripts!

NodeTypeAppearanceOrder=(
  NoGlobalsObjectNodes
  RegularObjectNodes
  UnassignedObjectNodes
  JSONInternalNodes
  DataNodes
  StubNodes
  EnumNodes
  DefinitionNodes
  GlobalDefinitionNodes
  InputOutputObjectNodes
  IOAndGlobalObjectNodes
)
declare -A NodeTypeDescriptions=(
[JSONInternalNodes]='Defined in the JSON Specs'
[DataNodes]='Plain data (string, number, etc.)'
[StubNodes]='Enum choices or similar'
[DefinitionNodes]='Nodes that are definitions'
[GlobalDefinitionNodes]='Nodes that contain defs used by most Objects'
[EnumNodes]='Enum Nodes'
[RegularObjectNodes]='Regular Objects (these need Global Defines)'
[IOAndGlobalObjectNodes]='Objects that need Global Defines and I/O info'
[InputOutputObjectNodes]='Objects that need I/O info'
[NoGlobalsObjectNodes]='Objects that do not need Global Defines'
[UnassignedObjectNodes]='Objects that have no defined role yet'
)
declare -A NodesByType=(
## Simple Node Types
[JSONInternalNodes]="IPAddress Time TimeLeft URI"
[DataNodes]="AheadRunning AheadWaiting Date Directory 
  EmailAddress File Format ID Label MD5Sum Name
  Path ResourcePayload SessionID Status Tags TextBlock
  Type Unit UserName UUID Value"
[StubNodes]="AllOf AnyOf Angle Attachment Conformation Dihedral
  Directory Distance File NoneOf OneOf Path RingPucker Rotamer
  SecondaryStructure TextBlock URI "
## Non-object nodes that refer to other nodes
[DefinitionNodes]="Resource"
[GlobalDefinitionNodes]="GlobalDefines GlobalActions GlobalMetadata"
[EnumNodes]="LogicGate GeometricProperty ResourceType"
## Objects
[RegularObjectNodes]="Atom Bond Fragment Geometry Linkage
  Molecule Represent Residue Selection Simulate User"
[IOAndGlobalObjectNodes]="AntibodyDocking Build GlycoComplex
  GlycoConjugate Image Job Sequence Text"
[InputOutputObjectNodes]="Resource"
[NoGlobalsObjectNodes]="Evaluate Options ReturnActions ReturnDryRun
  ReturnHelp ReturnOptions ReturnResponses ReturnSchema WebMetadata"
[UnassignedObjectNodes]="Project System"
)
declare -A NodeStylesByType=(
[NoGlobalsObjectNodes]='shape=octagon'
[RegularObjectNodes]='shape=octagon style=filled fillcolor="cadetblue2"'
[UnassignedObjectNodes]='shape=octagon style=filled fillcolor="khaki2"'
[JSONInternalNodes]='shape=parallelogram style="rounded"'
[DataNodes]='shape=parallelogram'
[StubNodes]='shape=rect style="rounded"'
[EnumNodes]='shape=diamond'
[DefinitionNodes]='shape=rect'
[GlobalDefinitionNodes]='shape=rect style=filled fillcolor="cadetblue2"'
[InputOutputObjectNodes]='shape=rect style=filled fillcolor="orchid1"'
[IOAndGlobalObjectNodes]='shape=octagon style=filled fillcolor="cadetblue2:orchid1"'
)

declare -A EdgeStylesByType=(
  [Single]='penwidth=1'
  [Double]='penwidth=4 color="gray" style="dashed"'
  [Multi]='penwidth=4 style="dotted"'
)
declare -A EdgeDescriptionsByType=(
  [Single]='Contains one'
  [Double]='Contains two (total, no matter how many tails)'
  [Multi]='Contains one or more'
)

declare -A SingleEntityRelations=(
  [Fragment]="Atom Residue"
  [Geometry]="GeometricProperty Selection Unit Value"
  [GeometricProperty]="Angle Conformation Dihedral Distance Rotamer RingPucker SecondaryStructure"
  [GlobalDefines]="GlobalActions GlobalMetadata"
  [GlobalActions]="Evaluate Options ReturnActions ReturnDryRun ReturnHelp ReturnOptions ReturnResponses ReturnSchema "
  [GlobalMetadata]="Format ID Label Name Type"
  [LogicGate]="AllOf OneOf AnyOf NoneOf"
  [Molecule]="Atom Residue "
  [Residue]="Atom "
  [Resource]="ResourcePayload ResourceType GlobalMetadata"
  [ResourceType]="Attachment Directory File Path TextBlock URI"
  [Selection]="LogicGate"
  [WebMetadata]="EmailAddress Date IPAddress SessionID Time User UserName UUID"
  [AntibodyDocking]="Build "
  [Build]="WebMetadata"
  [GlycoConjugate]="Build "
  [GlycoComplex]="AntibodyDocking Build"
  [Sequence]="MD5Sum"
  [Job]="AheadRunning AheadWaiting Date Status Time TimeLeft WebMetadata"
)
declare -A TwoEntityRelations=(
  [Bond]="Atom "
  [Linkage]="Molecule Residue"
)
declare -A MultipleEntityRelations=(
  [Fragment]="Atom Residue"
  [Molecule]="Atom Residue "
  [Residue]="Atom "
  [Selection]="Atom Bond Fragment Linkage Molecule Residue Selection"
  [AntibodyDocking]="Represent Sequence "
  [GlobalMetadata]="Tags"
  [GlycoConjugate]="Represent Sequence Simulate"
  [GlycoComplex]="Represent Sequence Simulate"
  [Represent]="Image Text"
  [Sequence]="Build Geometry Represent Simulate"
  [Simulate]="Job"
)
