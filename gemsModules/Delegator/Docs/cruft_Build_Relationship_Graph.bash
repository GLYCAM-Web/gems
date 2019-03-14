#!/bin/bash
##
## File Build_Relationship_Graph.bash begun on 2019-03-05 by BLFoley
## 
## Builds a simple graph for visualizing relationships as defined
## in the InputFile.
InputFile='JSON_API_Documentation_Data.bash'
OutputPREFIX='Relationship_Graph'
DotCommand="dot -Tsvg:cairo -o ${OutputPREFIX}.svg ${OutputPREFIX}.dot"
OUTFILE="${OutputPREFIX}.dot"

. ${InputFile}

exit

echo "digraph bigpicture {
  compound=true;
  rankdir=LR;

  node [ shape=star ]; // To make unspecified nodes obvious in the graph 
" > ${OUTFILE}
echo "
  // For objects " >> ${OUTFILE}
for i in ${NoGlobalsObjectNodes[@]} ; do
  echo "  ${i} [ shape=octagon ]; " >> ${OUTFILE}
done
for i in ${RegularObjectNodes[@]} ; do
  echo "  ${i} [ shape=octagon style=filled fillcolor=\"cadetblue2\" ]; " >> ${OUTFILE}
done
for i in ${UnassignedObjectNodes[@]} ; do
  echo "  ${i} [ shape=octagon style=filled fillcolor=\"khaki2\" ]; " >> ${OUTFILE}
done
echo "
  // I/O for plain data types (string, number, integer, etc.)
  // node [ shape=parallelogram ]; " >> ${OUTFILE}
for i in ${JSONInternalNodes[@]} ; do
  echo "  ${i} [ shape=parallelogram style=\"rounded\" ]; " >> ${OUTFILE}
done
for i in ${DataNodes[@]} ; do
  echo "  ${i} [ shape=parallelogram ]; " >> ${OUTFILE}
done
echo "
  // Stubs for enums
  // node [ shape=rect style=\"rounded\"]; " >> ${OUTFILE}
for i in ${StubNodes[@]} ; do
  echo "  ${i} [ shape=rect style=\"rounded\"]; " >> ${OUTFILE}
done
echo "
  // Enums
  // node [ shape=diamond ]; " >> ${OUTFILE}
for i in ${EnumNodes[@]} ; do
  echo "  ${i} [ shape=diamond ]; " >> ${OUTFILE}
done
echo "
  // For Definitions
  // node [ shape=rect ]; " >> ${OUTFILE}
for i in ${DefinitionNodes[@]} ; do
  echo "  ${i} [ shape=rect ]; " >> ${OUTFILE}
done
echo "
  // For Global Definitions
  // node [ shape=rect style=filled fillcolor=\"cadetblue2\" ]; " >> ${OUTFILE}
for i in ${GlobalDefinitionNodes[@]} ; do
  echo "  ${i} [ shape=rect style=filled fillcolor=\"cadetblue2\" ]; " >> ${OUTFILE}
done
for i in ${InputOutputObjectNodes[@]} ; do
  echo "  ${i} [ shape=octagon style=filled fillcolor=\"orchid1\" ]; " >> ${OUTFILE}
done
for i in ${IOAndGlobalObjectNodes[@]} ; do
  echo "  ${i} [ shape=octagon style=filled fillcolor=\"cadetblue2:orchid1\" ]; " >> ${OUTFILE}
done

for i in "${!SingleEntityRelations[@]}" ; do
  Value="${SingleEntityRelations[${i}]}"
  [[ "ZZZ${Value}" == "ZZZ" ]] && continue  ## skip if empty value 
  for j in ${Value} ; do
    echo "  ${i}->${j} [ penwidth=1 ];" >> ${OUTFILE}
  done
done

for i in "${!TwoEntityRelations[@]}" ; do
  Value="${TwoEntityRelations[${i}]}"
  [[ "ZZZ${Value}" == "ZZZ" ]] && continue  ## skip if empty value 
  for j in ${Value} ; do
    echo "  ${i}->${j} [ penwidth=4 color=\"gray\" style=\"dashed\" ];" >> ${OUTFILE}
  done
done

for i in "${!MultipleEntityRelations[@]}" ; do
  Value="${MultipleEntityRelations[${i}]}"
  [[ "ZZZ${Value}" == "ZZZ" ]] && continue  ## skip if empty value 
  for j in ${Value} ; do
    echo "  ${i}->${j} [ penwidth=4 style=\"dotted\" ];" >> ${OUTFILE}
  done
done

echo "

  Label->InputSpec [ style=invis ];
  Label->OutputSpec [ style=invis ];

  subgraph cluster_0 {
    label=\"Nodes Legend\";
    PlainObject [ shape=octagon label=\"Object\" ];
    GDObject [ shape=octagon style=filled fillcolor=\"cadetblue2\" label=\"Object with Global Defines\" ];
    IOGDObject [ shape=octagon style=filled fillcolor=\"cadetblue2:orchid1\" label=\"Object with Global Defines and I/O\" ];
    UnassignedObject [ shape=octagon style=filled fillcolor=\"khaki2\" label=\"Object with undecided fate\" ];
    Data [ shape=parallelogram ];
    JSONInternal [ shape=parallelogram style=\"rounded\" ];
    EnumChoice [ shape=rect style=\"rounded\"];
    Enum [ shape=diamond ];
    Definition [ shape=rect ];
  }

  subgraph cluster_1 {
    label=\"Edges Legend\";
    Single1 [ shape=none style=invis ];
    Single2 [ shape=none style=invis ];
    Single1->Single2 [ penwidth=1 label=\"Contains One\" ];
    Limit1 [ shape=none style=invis ];
    Limit2 [ shape=none style=invis ];
    Limit1->Limit2 [ penwidth=4 color=\"gray\" style=\"dashed\" label=\"Contains two\" ];
    Multi1 [ shape=none style=invis ];
    Multi2 [ shape=none style=invis ];
    Multi1->Multi2 [ penwidth=4 style=\"dotted\" label=\"Contains one or more\" ];
  }

  Data->Limit1 [ style=invis ];

}" >> ${OUTFILE}

eval ${DotCommand}
