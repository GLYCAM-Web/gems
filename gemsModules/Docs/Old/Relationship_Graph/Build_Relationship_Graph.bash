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
echo "digraph bigpicture {
  compound=true;
  rankdir=LR;

  node [ shape=star ]; // To make unspecified nodes obvious in the graph 
" > ${OUTFILE}
for NodeType in ${NodeTypeAppearanceOrder[@]} ; do
  ##echo "node type is ${NodeType} "
  echo "  // ${NodeTypeDescriptions[${NodeType}]} " >> ${OUTFILE}
  for Node in ${NodesByType[${NodeType}]} ; do
    ##echo "Node ${Node} is type ${NodeType}"
    echo "  ${Node} [ ${NodeStylesByType[${NodeType}]} ];" >> ${OUTFILE}
  done
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

echo '

  subgraph cluster_0 {
    label="Nodes Legend"; ' >> ${OUTFILE}
for NodeType in ${NodeTypeAppearanceOrder[@]} ; do
  echo "  ${NodeType} [ ${NodeStylesByType[${NodeType}]} label=\"${NodeTypeDescriptions[${NodeType}]}\" ];" >> ${OUTFILE}
done
echo '  } ' >> ${OUTFILE}

echo '
  subgraph cluster_1 {
    label="Edges Legend"; ' >> ${OUTFILE}
for DummyNode in "${!EdgeStylesByType[@]}" ; do
  Style="${EdgeStylesByType[${DummyNode}]}"
  Description="${EdgeDescriptionsByType[${DummyNode}]}"
  echo "  ${DummyNode}1 [ shape=none style=invis ] ; 
  ${DummyNode}2 [ shape=none style=invis ] ; 
  ${DummyNode}1->${DummyNode}2 [ ${Style} label=\"${Description}\" ] ; " >> ${OUTFILE}
done
echo '  } 

  DataNodes->Double1 [ style=invis ];

}' >> ${OUTFILE}

eval ${DotCommand}
