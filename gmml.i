/* File: gmml.i */
%module gmml
%include <std_string.i>
%include <std_iostream.i>
%include<std_map.i>
%include<std_vector.i>

%{
#define SWIG_FILE_WITH_INIT
//#include "/usr/include/sql.h"
//#include "/usr/include/sqlext.h"

#include "gmml/includes/common.hpp"
#include "gmml/includes/InputSet/CoordinateFileSpace/coordinatefile.hpp"
#include "gmml/includes/InputSet/CoordinateFileSpace/coordinatefileprocessingexception.hpp"
#include "gmml/includes/GeometryTopology/coordinate.hpp"
#include "gmml/includes/GeometryTopology/plane.hpp"
#include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfile.hpp"
#include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileatom.hpp"
#include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileprocessingexception.hpp"
#include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileresidue.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfile.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileangle.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileatom.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfilebond.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfiledihedral.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfiledihedralterm.hpp"
#include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileprocessingexception.hpp"
#include "gmml/includes/ParameterSet/PrepFileSpace/prepfile.hpp"
#include "gmml/includes/ParameterSet/PrepFileSpace/prepfileatom.hpp"
#include "gmml/includes/ParameterSet/PrepFileSpace/prepfileresidue.hpp"
#include "gmml/includes/ParameterSet/PrepFileSpace/prepfileprocessingexception.hpp"

#include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceprocessingexception.hpp"
#include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceresidue.hpp"
#include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceamberprepresidue.hpp"
#include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequence.hpp"

//#include "gmml/includes/InputSet/CifFileSpace/ciffileatom.hpp"
//#include "gmml/includes/InputSet/CifFileSpace/ciffile.hpp"
//#include "gmml/includes/InputSet/CifFileSpace/ciffileprocessingexception.hpp"

#include "gmml/includes/InputSet/PdbFileSpace/pdbatom.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbatomcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbcompoundcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbcompoundspecification.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbconnectcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbcrystallographiccard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfidebondcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfideresidue.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfideresiduebond.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbfile.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbfileprocessingexception.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbformula.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbformulacard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheadercard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbhelix.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbhelixcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbhelixresidue.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogen.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogenatomcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogencard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogenname.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogennamecard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogensynonym.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbheterogensynonymcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdblink.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdblinkcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdblinkresidue.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmatrixn.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmatrixncard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmodel.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmodelcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmodelresidueset.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbmodeltypecard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbnummodelcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdboriginxn.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdboriginxncard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbresiduemodification.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbresiduemodificationcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbresiduesequence.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbresiduesequencecard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbscalen.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbscalencard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsheet.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsheetcard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsheetstrand.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsheetstrandresidue.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsite.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsitecard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbsiteresidue.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbtitlecard.hpp"
#include "gmml/includes/InputSet/PdbFileSpace/pdbresidue.hpp"

#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtatom.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtatomcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtbranchcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtcompoundcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtfile.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtfileprocessingexception.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodel.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodelcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodelresidueset.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtremarkcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtrootcard.hpp"
#include "gmml/includes/InputSet/PdbqtFileSpace/pdbqttorsionaldofcard.hpp"

#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessor.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorchaintermination.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessordisulfidebond.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorhistidinemapping.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessormissingresidue.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorreplacedhydrogen.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorunrecognizedheavyatom.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorunrecognizedresidue.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessoralternateresidue.hpp"
#include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorresidueinfo.hpp"

#include "gmml/includes/GeometryTopology/InternalCoordinate/angle.hpp"
#include "gmml/includes/GeometryTopology/InternalCoordinate/dihedral.hpp"
#include "gmml/includes/GeometryTopology/InternalCoordinate/distance.hpp"

#include "gmml/includes/MolecularModeling/element.hpp"
#include "gmml/includes/MolecularModeling/dockingatom.hpp"
#include "gmml/includes/MolecularModeling/moleculardynamicatom.hpp"
#include "gmml/includes/MolecularModeling/quantommechanicatom.hpp"
#include "gmml/includes/MolecularModeling/atom.hpp"
#include "gmml/includes/MolecularModeling/residue.hpp"
#include "gmml/includes/MolecularModeling/atomnode.hpp"
#include "gmml/includes/MolecularModeling/assembly.hpp"

#include "gmml/includes/GeometryTopology/grid.hpp"
#include "gmml/includes/GeometryTopology/cell.hpp"

#include "gmml/includes/InputSet/TopologyFileSpace/topologyangle.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyangletype.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyassembly.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyatom.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyatompair.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologybond.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologybondtype.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologydihedral.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologydihedraltype.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyfile.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyresidue.hpp"
#include "gmml/includes/InputSet/TopologyFileSpace/topologyfileprocessingexception.hpp"

%}

%inline %{
std::ostream & get_cout() { return std::cout; }
%}

//%include "/usr/include/sql.h"
//%include "/usr/include/sqlext.h"

%include "gmml/includes/common.hpp"
%include "gmml/includes/InputSet/CoordinateFileSpace/coordinatefile.hpp"
%include "gmml/includes/InputSet/CoordinateFileSpace/coordinatefileprocessingexception.hpp"
%include "gmml/includes/GeometryTopology/coordinate.hpp"
%include "gmml/includes/GeometryTopology/plane.hpp"
%include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfile.hpp"
%include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileatom.hpp"
%include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileprocessingexception.hpp"
%include "gmml/includes/ParameterSet/LibraryFileSpace/libraryfileresidue.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfile.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileangle.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileatom.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfilebond.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfiledihedral.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfiledihedralterm.hpp"
%include "gmml/includes/ParameterSet/ParameterFileSpace/parameterfileprocessingexception.hpp"
%include "gmml/includes/ParameterSet/PrepFileSpace/prepfile.hpp"
%include "gmml/includes/ParameterSet/PrepFileSpace/prepfileatom.hpp"
%include "gmml/includes/ParameterSet/PrepFileSpace/prepfileresidue.hpp"
%include "gmml/includes/ParameterSet/PrepFileSpace/prepfileprocessingexception.hpp"

%include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceprocessingexception.hpp"
%include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceresidue.hpp"
%include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequenceamberprepresidue.hpp"
%include "gmml/includes/InputSet/CondensedSequenceSpace/condensedsequence.hpp"

%include "gmml/includes/InputSet/PdbFileSpace/pdbatom.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbatomcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbcompoundcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbcompoundspecification.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbconnectcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbcrystallographiccard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfidebondcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfideresidue.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbdisulfideresiduebond.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbfile.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbfileprocessingexception.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbformula.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbformulacard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheadercard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbhelix.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbhelixcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbhelixresidue.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogen.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogenatomcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogencard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogenname.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogennamecard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogensynonym.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbheterogensynonymcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdblink.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdblinkcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdblinkresidue.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmatrixn.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmatrixncard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmodel.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmodelcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmodelresidueset.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbmodeltypecard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbnummodelcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdboriginxn.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdboriginxncard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbresiduemodification.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbresiduemodificationcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbresiduesequence.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbresiduesequencecard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbscalen.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbscalencard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsheet.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsheetcard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsheetstrand.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsheetstrandresidue.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsite.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsitecard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbsiteresidue.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbtitlecard.hpp"
%include "gmml/includes/InputSet/PdbFileSpace/pdbresidue.hpp"

%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtatom.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtatomcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtbranchcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtcompoundcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtfile.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtfileprocessingexception.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodel.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodelcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtmodelresidueset.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtremarkcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqtrootcard.hpp"
%include "gmml/includes/InputSet/PdbqtFileSpace/pdbqttorsionaldofcard.hpp"

//%include "gmml/includes/InputSet/CifFileSpace/ciffileatom.hpp"
//%include "gmml/includes/InputSet/CifFileSpace/ciffile.hpp"
//%include "gmml/includes/InputSet/CifFileSpace/ciffileprocessingexception.hpp"

%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessor.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorchaintermination.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessordisulfidebond.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorhistidinemapping.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessormissingresidue.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorreplacedhydrogen.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorunrecognizedheavyatom.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorunrecognizedresidue.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessoralternateresidue.hpp"
%include "gmml/includes/Resolver/PdbPreprocessor/pdbpreprocessorresidueinfo.hpp"

%include "gmml/includes/GeometryTopology/InternalCoordinate/angle.hpp"
%include "gmml/includes/GeometryTopology/InternalCoordinate/dihedral.hpp"
%include "gmml/includes/GeometryTopology/InternalCoordinate/distance.hpp"

%include "gmml/includes/MolecularModeling/element.hpp"
%include "gmml/includes/MolecularModeling/dockingatom.hpp"
%include "gmml/includes/MolecularModeling/moleculardynamicatom.hpp"
%include "gmml/includes/MolecularModeling/quantommechanicatom.hpp"
%include "gmml/includes/MolecularModeling/atom.hpp"
%include "gmml/includes/MolecularModeling/residue.hpp"
%include "gmml/includes/MolecularModeling/atomnode.hpp"
%include "gmml/includes/MolecularModeling/assembly.hpp"

%include "gmml/includes/GeometryTopology/grid.hpp"
%include "gmml/includes/GeometryTopology/cell.hpp"

%include "gmml/includes/InputSet/TopologyFileSpace/topologyangle.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyangletype.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyassembly.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyatom.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyatompair.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologybond.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologybondtype.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologydihedral.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologydihedraltype.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyfile.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyresidue.hpp"
%include "gmml/includes/InputSet/TopologyFileSpace/topologyfileprocessingexception.hpp"

%template(string_vector) std::vector<std::string>;
%template(int_vector) std::vector<int>;
%template(double_vector) std::vector<double>;
%template(char_vector) std::vector<char>;
%template(bool_vector) std::vector<bool>;
//std::vector<Dihedral> improper_dihedrals_;
%template(dihedral_vector) std::vector<std::vector<std::string> >;

///GeometryTopology///
//std::vector<GeometryTopology::Coordinate*> coordinates_;
%template(coordinate_vector) std::vector<GeometryTopology::Coordinate*>;

//typedef std::vector<Cell*> CellVector;
%template(cell_vector) std::vector<GeometryTopology::Cell*>;


///Prep File///
//std::vector<PrepFileAtom*> atoms_;
%template(prepfileatom_vector) std::vector<PrepFileSpace::PrepFileAtom*>;


///Parameter File///
%template() std::pair<std::string, ParameterFileSpace::ParameterFileAtom*>;
%template(atoms_map_parameter_file) std::map<std::string, ParameterFileSpace::ParameterFileAtom*>;

%template() std::pair<std::vector<std::string>, ParameterFileSpace::ParameterFileBond*>;
%template(bonds_map_parameter_file) std::map<std::vector<std::string>, ParameterFileSpace::ParameterFileBond*>;

%template() std::pair<std::vector<std::string>, ParameterFileSpace::ParameterFileAngle*>;
%template(angles_map_parameter_file) std::map<std::vector<std::string>, ParameterFileSpace::ParameterFileAngle*>;

//std::vector<ParameterFileDihedralTerm> terms_;
%template(dihedral_terms_vector_parameter_file) std::vector<ParameterFileSpace::ParameterFileDihedralTerm>;
%template() std::pair<std::vector<std::string>, ParameterFileSpace::ParameterFileDihedral*>;
%template(dihedrals_map_parameter_file) std::map<std::vector<std::string>, ParameterFileSpace::ParameterFileDihedral*>;


///Library File///
//typedef std::map<std::string, LibraryFileResidue*> ResidueMap;
%template() std::pair<std::string, LibraryFileSpace::LibraryFileResidue*>;
%template(residue_map_library_file) std::map<std::string, LibraryFileSpace::LibraryFileResidue*>;

//typedef std::map<int, LibraryFileAtom*> AtomMap;
%template() std::pair<int, LibraryFileSpace::LibraryFileAtom*>;
%template(atom_map_library_file) std::map<int, LibraryFileSpace::LibraryFileAtom*>;


///Prep File///
//typedef std::map<int, int> Loop;
%template() std::pair<int,int>;
%template(loop_map_prep_file) std::map<int, int>;

//typedef std::map< std::string, PrepFileResidue* > ResidueMap;
%template() std::pair<std::string, PrepFileSpace::PrepFileResidue*>;
%template(residue_map_prep_file) std::map<std::string, PrepFileSpace::PrepFileResidue*>;


///PDB file///
//typedef std::map<int, PdbAtom*> PdbAtomMap;
%template() std::pair<int, PdbFileSpace::PdbAtom*>;
%template(atom_map_pdb_file) std::map<int, PdbFileSpace::PdbAtom*>;

//typedef std::map<std::string, PdbCompoundSpecification*> PdbCompoundSpecificationMap;
%template() std::pair<std::string, PdbFileSpace::PdbCompoundSpecification*>;
%template(compound_specification_map_pdb_file) std::map<std::string, PdbFileSpace::PdbCompoundSpecification*>;

//typedef std::map<int, std::vector<int> > BondedAtomsSerialNumbersMap;
%template() std::pair<int, std::vector<int> >;
%template(bonded_atoms_serial_numbers_map_pdb_file) std::map<int, std::vector<int> >;

//typedef std::map<int, PdbDisulfideResidueBond*> DisulfideResidueBondMap;
%template() std::pair<int, PdbFileSpace::PdbDisulfideResidueBond*>;
%template(disulfide_residue_bond_map_pdb_file) std::map<int, PdbFileSpace::PdbDisulfideResidueBond*>;

//typedef std::vector<PdbDisulfideResidue*> DisulfideResidueVector;
%template(pdbdisulfideresidue_vector) std::vector<PdbFileSpace::PdbDisulfideResidue*>;

//typedef std::map<std::string, PdbFormula*> FormulaMap;
%template() std::pair<std::string, PdbFileSpace::PdbFormula*>;
%template(formula_map_pdb_file) std::map<std::string, PdbFileSpace::PdbFormula*>;

//typedef std::vector<PdbHelixResidue*> HelixResidueVector;
%template(pdbhelixresidue_vector) std::vector<PdbFileSpace::PdbHelixResidue*>;

//typedef std::map<std::string, PdbHelix*> HelixMap;
%template() std::pair<std::string, PdbFileSpace::PdbHelix*>;
%template(helix_map_pdb_file) std::map<std::string, PdbFileSpace::PdbHelix*>;

//typedef PdbAtom PdbHeterogenAtom;
///???
      
//typedef std::map<int, PdbHeterogenAtom*> PdbHeterogenAtomMap;
//%template() std::pair<int, PdbFileSpace::PdbHeterogenAtomCard::PdbHeterogenAtom*>;
//%template(heterogen_atom_map_pdb_file) std::map<int, PdbFileSpace::PdbHeterogenAtomCard::PdbHeterogenAtom*>;

//typedef std::map<std::string, PdbHeterogen*> HeterogenMap;
%template() std::pair<std::string, PdbFileSpace::PdbHeterogen*>;
%template(heterogen_pdb_map_file) std::map<std::string, PdbFileSpace::PdbHeterogen*>;

//typedef std::map<std::string, PdbHeterogenName*> HeterogenNameMap;
%template() std::pair<std::string, PdbFileSpace::PdbHeterogenName*>;
%template(heterogen_name_map_pdb_file) std::map<std::string, PdbFileSpace::PdbHeterogenName*>;

//typedef std::map<std::string, PdbHeterogenSynonym*> HeterogenSynonymMap;
%template() std::pair<std::string, PdbFileSpace::PdbHeterogenSynonym*>;
%template(heterogen_synonym_map_pdb_file) std::map<std::string, PdbFileSpace::PdbHeterogenSynonym*>;

//typedef std::vector< PdbLinkResidue* > LinkResidueVector;
%template(pdblinkresidue_vector) std::vector<PdbFileSpace::PdbLinkResidue*>;

//typedef std::vector< PdbLink* > LinkVector;
%template(pdblink_vector) std::vector<PdbFileSpace::PdbLink*>;

//typedef std::vector<PdbMatrixN*> MatrixNVector;
%template(pdbmatrixn_vector) std::vector<PdbFileSpace::PdbMatrixN*>;

//typedef std::vector<MatrixNVector> MatrixNVectorVector;
%template(pdbmatrixn_vector_vector) std::vector<PdbFileSpace::PdbMatrixNCard::MatrixNVector>;

//typedef std::map<int, PdbModel*> PdbModelMap;
%template() std::pair<int, PdbFileSpace::PdbModel*>;
%template(model_map_pdb_file) std::map<int, PdbFileSpace::PdbModel*>;

//typedef std::vector<PdbAtomCard*> AtomCardVector;
%template(pdbatomcard_vector) std::vector<PdbFileSpace::PdbAtomCard*>;

//typedef std::vector<PdbHeterogenAtomCard*> HeterogenAtomCardVector;
%template(pdbheterogenatomcard_vector) std::vector<PdbFileSpace::PdbHeterogenAtomCard*>;

//typedef std::vector< PdbOriginXn* > OriginXnVector;
%template(pdboriginxn_vector) std::vector<PdbFileSpace::PdbOriginXn*>;

//typedef std::map<std::string, PdbResidueModification*> ResidueModificationMap;
%template() std::pair<std::string, PdbFileSpace::PdbResidueModification*>;
%template(residue_modification_map_pdb_file) std::map<std::string, PdbFileSpace::PdbResidueModification*>;

//typedef std::map<char, PdbResidueSequence*> ResidueSequenceMap;
%template() std::pair<char, PdbFileSpace::PdbResidueSequence*>;
%template(residue_sequence_map_pdb_file) std::map<char, PdbFileSpace::PdbResidueSequence*>;

//typedef std::vector< PdbScaleN* > ScaleNVector;
%template(pdbscalenvector_vector) std::vector<PdbFileSpace::PdbScaleN*>;

//typedef std::vector<PdbSheetStrand*> SheetStrandVector;
%template(pdbsheetstrand_vector) std::vector<PdbFileSpace::PdbSheetStrand*>;

//typedef std::map<std::string, PdbSheet*> SheetMap;
%template() std::pair<std::string, PdbFileSpace::PdbSheet*>;
%template(sheet_pdb_map_file) std::map<std::string, PdbFileSpace::PdbSheet*>;

//typedef std::vector<PdbSheetStrandResidue*> SheetStrandResidueVector;
%template(pdbsheetstrandresidue_vector) std::vector<PdbFileSpace::PdbSheetStrandResidue*>;

//typedef std::vector< PdbSiteResidue* > SiteResidueVector;
%template(pdbsiteresidue_vector) std::vector<PdbFileSpace::PdbSiteResidue*>;

//typedef std::map<std::string, PdbSite*> PdbSiteMap;
%template() std::pair<std::string, PdbFileSpace::PdbSite*>;
%template(site_map_pdb_file) std::map<std::string, PdbFileSpace::PdbSite*>;

//typedef std::vector<PdbAtom*> PdbAtomVector;
%template(pdb_atom_vector) std::vector<PdbFileSpace::PdbAtom*>;


///PDB Preprocessor///
//typedef std::vector<PdbPreprocessorDisulfideBond*> PdbPreprocessorDisulfideBondVector;
%template(pdbpreprocessordisulfidebond_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorDisulfideBond*>;

//typedef std::vector<PdbPreprocessorChainTermination*> PdbPreprocessorChainTerminationVector;
%template(pdbpreprocessorchaintermination_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorChainTermination*>;

//typedef std::vector<PdbPreprocessorHistidineMapping*> PdbPreprocessorHistidineMappingVector;
%template(pdbpreprocessorhistidinemapping_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorHistidineMapping*>;

//typedef std::vector<PdbPreprocessorMissingResidue*> PdbPreprocessorMissingResidueVector;
%template(pdbpreprocessormissingresidue_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorMissingResidue*>;

//typedef std::vector<PdbPreprocessorUnrecognizedResidue*> PdbPreprocessorUnrecognizedResidueVector;
%template(pdbpreprocessorunrecognizedresidue_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorUnrecognizedResidue*>;

//typedef std::vector<PdbPreprocessorUnrecognizedHeavyAtom*> PdbPreprocessorUnrecognizedHeavyAtomVector;
%template(pdbpreprocessorunrecognizedheavyatom_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorUnrecognizedHeavyAtom*>;

//typedef std::vector<PdbPreprocessorReplacedHydrogen*> PdbPreprocessorReplacedHydrogenVector;
%template(pdbpreprocessorreplacedhydrogen_vector) std::vector<PdbPreprocessorSpace::PdbPreprocessorReplacedHydrogen*>;

//typedef std::map<std::string, PdbPreprocessorAlternateResidue*> PdbPreprocessorAlternateResidueMap;
%template() std::pair<std::string, PdbPreprocessorSpace::PdbPreprocessorAlternateResidue*>;
%template(alternate_residue_map_pdbpreprocessor_file) std::map<std::string, PdbPreprocessorSpace::PdbPreprocessorAlternateResidue*>;

//typedef std::map<std::string, PdbPreprocessorResidueInfo*> PdbPreprocessorResidueInfoMap;
%template() std::pair<std::string, PdbPreprocessorSpace::PdbPreprocessorResidueInfo*>;
%template(residue_info_map_pdbpreprocessor_file) std::map<std::string, PdbPreprocessorSpace::PdbPreprocessorResidueInfo*>;


///MolecularModeling///
//typedef std::vector<Assembly*> AssemblyVector;
%template(assembly_vector) std::vector<MolecularModeling::Assembly* >;

//typedef std::vector<Residue*> ResidueVector;
%template(residue_vector) std::vector<MolecularModeling::Residue* >;  

//typedef std::vector<Atom*> AtomVector;
%template(atom_vector) std::vector<MolecularModeling::Atom* >;  

//typedef std::vector<AtomVector > AtomVectorVector;
//%template(atom_vector_vector) std::vector<std::vector<MolecularModeling::Atom* > >;

//typedef std::map<std::string, AtomVector> CycleMap;
%template() std::pair<std::string, std::vector<MolecularModeling::Atom* > >;
%template(cycle_map_assembly_file) std::map<std::string, std::vector<MolecularModeling::Atom* > >;

//typedef std::vector<Glycan::Oligosaccharide*> OligosaccharideVector;
%template(oligosaccharide_vector) std::vector<Glycan::Oligosaccharide* >;  


///Topology File///
//typedef std::map<std::string, TopologyResidue*> TopologyResidueMap;
%template() std::pair<std::string, TopologyFileSpace::TopologyResidue*>;
%template(residue_map_Topology_file) std::map<std::string, TopologyFileSpace::TopologyResidue*>;

//typedef std::map<std::vector<std::string>, TopologyBond*> TopologyBondMap;
%template() std::pair<std::string, TopologyFileSpace::TopologyBond*>;
%template(bond_map_Topology_file) std::map<std::string, TopologyFileSpace::TopologyBond*>;

//typedef std::map<std::vector<std::string>, TopologyAngle*> TopologyAngleMap;
%template() std::pair<std::string, TopologyFileSpace::TopologyAngle*>;
%template(angle_map_Topology_file) std::map<std::string, TopologyFileSpace::TopologyAngle*>;

//typedef std::map<std::vector<std::string>, TopologyDihedral*> TopologyDihedralMap;
%template() std::pair<std::string, TopologyFileSpace::TopologyDihedral*>;
%template(dihedral_map_Topology_file) std::map<std::string, TopologyFileSpace::TopologyDihedral*>;

//typedef std::map<int, double> TopologyCoefficientMap;
%template() std::pair<int, double>;
%template(coefficient_map_Topology_file) std::map<int, double>;

//typedef std::map<int, TopologyAtomType*> TopologyAtomPairMap;
%template() std::pair<std::string, TopologyFileSpace::TopologyAtomPair*>;
%template(atom_pair_map_Topology_file) std::map<std::string, TopologyFileSpace::TopologyAtomPair*>;

//typedef std::map<int, TopologyBondType*> TopologyBondTypeMap;
%template() std::pair<int, TopologyFileSpace::TopologyBondType*>;
%template(bond_type_map_Topology_file) std::map<int, TopologyFileSpace::TopologyBondType*>;

//typedef std::map<int, TopologyAngleType*> TopologyAngleTypeMap;
%template() std::pair<int, TopologyFileSpace::TopologyAngleType*>;
%template(angle_type_map_Topology_file) std::map<int, TopologyFileSpace::TopologyAngleType*>;

//typedef std::map<int, TopologyDihedralType*> TopologyDihedralTypeMap;
%template() std::pair<int, TopologyFileSpace::TopologyDihedralType*>;
%template(dihedral_type_map_Topology_file) std::map<int, TopologyFileSpace::TopologyDihedralType*>;


///PDBQT file///
//typedef std::map<std::string, PdbAtomVector* > PdbResidueAtomsMap;
%template() std::pair<std::string, PdbFileSpace::PdbFile::PdbAtomVector* >;
%template(pdb_residue_atom_map) std::map<std::string, PdbFileSpace::PdbFile::PdbAtomVector* >;

//typedef std::vector<PdbqtAtom*> PdbqtAtomVector;
%template(pdbqt_atom_vector) std::vector<PdbqtFileSpace::PdbqtAtom*>;

//typedef std::map<std::string, PdbqtAtomVector* > PdbqtResidueAtomsMap;
%template() std::pair<std::string, PdbqtFileSpace::PdbqtFile::PdbqtAtomVector*>;
%template(pdbqt_residue_atom_map) std::map<std::string, PdbqtFileSpace::PdbqtFile::PdbqtAtomVector*>;

//typedef std::map<int, PdbqtModel*> PdbqtModelMap;
%template() std::pair<int, PdbqtFileSpace::PdbqtModel*>;
%template(pdbqt_model_map) std::map<int, PdbqtFileSpace::PdbqtModel*>;

//typedef std::vector<PdbqtRemarkCard*> RemarkCardVector;
%template(pdbqt_remark_card_vector) std::vector<PdbqtFileSpace::PdbqtRemarkCard*>;

//typedef std::vector<PdbqtTorsionalDoFCard*> TorsionalDoFCardVector;
%template(torsional_dof_card_vector) std::vector<PdbqtFileSpace::PdbqtTorsionalDoFCard*>;

//typedef std::map<int, PdbqtAtom*> PdbqtAtomMap;
%template() std::pair<int, PdbqtFileSpace::PdbqtAtom* >;
%template(pdbqt_atom_map) std::map<int, PdbqtFileSpace::PdbqtAtom* >;

//typedef std::vector<PdbqtBranchCard*> BranchCardVector;
%template(pdbqt_branch_card_vector) std::vector<PdbqtFileSpace::PdbqtBranchCard*>;

///Cif File///
//typedef std::vector<CifFileAtom*> CifFileAtomVector;
//%template(cif_atom_vector) std::vector<CifFileSpace::CifFileAtom*>;

///Condensed Sequence///
//typedef std::vector<CondensedSequenceResidue*> CondensedSequenceResidueVector;
//%template(condensedsequence_residue_vector) std::vector<CondensedSequenceSpace::CondensedSequenceResidue*>;

//typedef std::vector<gmml::CondensedSequenceTokenType> CondensedSequenceTokenTypeVector;
//%template(condensedsequence_token_type_vector) std::vector<gmml::CondensedSequenceTokenType>;

//typedef std::vector<CondensedSequenceResidue*> CondensedSequenceResidueTree;
%template(condensedsequence_residue_tree) std::vector<CondensedSequenceSpace::CondensedSequenceResidue*>;

//typedef std::vector<CondensedSequenceAmberPrepResidue*> CondensedSequenceAmberPrepResidueTree;
%template(condensedsequence_amber_prep_residue_tree) std::vector<CondensedSequenceSpace::CondensedSequenceAmberPrepResidue*>;

//typedef std::pair<std::string, RotamersAndGlycosidicAnglesInfo*> RotamerNameInfoPair;
%template(rotamer_name_info_pair) std::pair<std::string, CondensedSequenceSpace::RotamersAndGlycosidicAnglesInfo*>;

//typedef std::vector<RotamerNameInfoPair> CondensedSequenceRatomersAndGlycosidicAnglesInfo;
%template(rotamer_angle_info_vector) std::vector<std::pair<std::string, CondensedSequenceSpace::RotamersAndGlycosidicAnglesInfo*> >;

//std::pair<std::string, double>
%template(string_double_pair) std::pair<std::string, double>;

//std::vector<std::pair<std::string, double> >
%template(glycosidic_angle_name_value_pair_vector) std::vector<std::pair<std::string, double> >;

//std::pair<std::string, std::vector<std::string> >
%template(string_vector_string_pair) std::pair<std::string, std::vector<std::string> >;

//std::vector<std::pair<std::string, std::vector<std::string> > >
%template(string_vector_string_pair_vector) std::vector<std::pair<std::string, std::vector<std::string> > >;

%template(vector_vector_int) std::vector<std::vector<int> >;

//std::vector<std::vector<double> >
%template(vector_vector_double) std::vector<std::vector<double> >;

//typedef std::map<int, std::vector<std::vector<double> > > IndexLinkageConfigurationMap;
%template() std::pair<int, std::vector<std::vector<double> > >;
%template(int_vector_vector_double_map) std::map<int, std::vector<std::vector<double> > >;

//typedef std::map<int, std::string> IndexNameMap;
%template() std::pair<int, std::string>;
%template(int_string_map) std::map<int, std::string>;

//typedef std::map<int, std::string> DerivativeMap;
//%template() std::pair<int, std::string >;
//%template(condensedsequence_derivative_map) std::map<int, std::string >;

///Common///
//typedef std::map<std::string, std::string> ResidueNameMap;
%template() std::pair<std::string, std::string>;
%template(residue_name_map) std::map<std::string, std::string>;

///Utils///
//typedef std::map<int, std::vector<Glycan::SugarName> > SugarNameClosestMatchMap;
//%template() std::pair<int, std::vector<Glycan::SugarName> >;
//%template(sugar_name_closest_match_map) std::map<int, std::vector<Glycan::SugarName> >;
