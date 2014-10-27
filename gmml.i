/* File: gmml.i */
%module gmml
%include <std_string.i>
%include <std_iostream.i>
%include<std_map.i>
%include<std_vector.i>

%{
#define SWIG_FILE_WITH_INIT
#include "gmml/includes/common.hpp"
#include "gmml/includes/FileSet/CoordinateFileSpace/coordinatefile.hpp"
#include "gmml/includes/FileSet/CoordinateFileSpace/coordinatefileprocessingexception.hpp"
#include "gmml/includes/Geometry/coordinate.hpp"
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

#include "gmml/includes/FileSet/PdbFileSpace/pdbatom.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbatomcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbcompoundcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbcompoundspecification.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbconnectcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbcrystallographiccard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfidebondcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfideresidue.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfideresiduebond.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbfile.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbfileprocessingexception.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbformula.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbformulacard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheadercard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbhelix.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbhelixcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbhelixresidue.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogen.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogenatomcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogencard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogenname.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogennamecard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogensynonym.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbheterogensynonymcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdblink.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdblinkcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdblinkresidue.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmatrixn.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmatrixncard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmodel.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmodelcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmodelresidueset.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbmodeltypecard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbnummodelcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdboriginxn.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdboriginxncard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbresiduemodification.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbresiduemodificationcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbresiduesequence.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbresiduesequencecard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbscalen.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbscalencard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsheet.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsheetcard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsheetstrand.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsheetstrandresidue.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsite.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsitecard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbsiteresidue.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbtitlecard.hpp"
#include "gmml/includes/FileSet/PdbFileSpace/pdbresidue.hpp"

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

#include "gmml/includes/Geometry/InternalCoordinate/angle.hpp"
#include "gmml/includes/Geometry/InternalCoordinate/dihedral.hpp"
#include "gmml/includes/Geometry/InternalCoordinate/distance.hpp"

#include "gmml/includes/MolecularModeling/element.hpp"
#include "gmml/includes/MolecularModeling/dockingatom.hpp"
#include "gmml/includes/MolecularModeling/moleculardynamicatom.hpp"
#include "gmml/includes/MolecularModeling/quantommechanicatom.hpp"
#include "gmml/includes/MolecularModeling/atom.hpp"
#include "gmml/includes/MolecularModeling/residue.hpp"
#include "gmml/includes/MolecularModeling/atomnode.hpp"
#include "gmml/includes/MolecularModeling/assembly.hpp"

#include "gmml/includes/FileSet/TopologyFileSpace/topologyangle.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyangletype.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyassembly.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyatom.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyatompair.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologybond.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologybondtype.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologydihedral.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologydihedraltype.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyfile.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyresidue.hpp"
#include "gmml/includes/FileSet/TopologyFileSpace/topologyfileprocessingexception.hpp"
%}

%inline %{
std::ostream & get_cout() { return std::cout; }
%}

%include "gmml/includes/common.hpp"
%include "gmml/includes/FileSet/CoordinateFileSpace/coordinatefile.hpp"
%include "gmml/includes/FileSet/CoordinateFileSpace/coordinatefileprocessingexception.hpp"
%include "gmml/includes/Geometry/coordinate.hpp"
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

%include "gmml/includes/FileSet/PdbFileSpace/pdbatom.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbatomcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbcompoundcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbcompoundspecification.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbconnectcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbcrystallographiccard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfidebondcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfideresidue.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbdisulfideresiduebond.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbfile.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbfileprocessingexception.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbformula.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbformulacard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheadercard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbhelix.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbhelixcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbhelixresidue.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogen.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogenatomcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogencard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogenname.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogennamecard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogensynonym.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbheterogensynonymcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdblink.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdblinkcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdblinkresidue.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmatrixn.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmatrixncard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmodel.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmodelcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmodelresidueset.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbmodeltypecard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbnummodelcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdboriginxn.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdboriginxncard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbresiduemodification.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbresiduemodificationcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbresiduesequence.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbresiduesequencecard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbscalen.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbscalencard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsheet.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsheetcard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsheetstrand.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsheetstrandresidue.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsite.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsitecard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbsiteresidue.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbtitlecard.hpp"
%include "gmml/includes/FileSet/PdbFileSpace/pdbresidue.hpp"

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

%include "gmml/includes/Geometry/InternalCoordinate/angle.hpp"
%include "gmml/includes/Geometry/InternalCoordinate/dihedral.hpp"
%include "gmml/includes/Geometry/InternalCoordinate/distance.hpp"

%include "gmml/includes/MolecularModeling/element.hpp"
%include "gmml/includes/MolecularModeling/dockingatom.hpp"
%include "gmml/includes/MolecularModeling/moleculardynamicatom.hpp"
%include "gmml/includes/MolecularModeling/quantommechanicatom.hpp"
%include "gmml/includes/MolecularModeling/atom.hpp"
%include "gmml/includes/MolecularModeling/residue.hpp"
%include "gmml/includes/MolecularModeling/atomnode.hpp"
%include "gmml/includes/MolecularModeling/assembly.hpp"

%include "gmml/includes/FileSet/TopologyFileSpace/topologyangle.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyangletype.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyassembly.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyatom.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyatompair.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologybond.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologybondtype.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologydihedral.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologydihedraltype.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyfile.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyresidue.hpp"
%include "gmml/includes/FileSet/TopologyFileSpace/topologyfileprocessingexception.hpp"

%template(string_vector) std::vector<std::string>;
%template(int_vector) std::vector<int>;
%template(double_vector) std::vector<double>;
%template(char_vector) std::vector<char>;
%template(bool_vector) std::vector<bool>;
//std::vector<PrepFileAtom*> atoms_;
%template(prepfileatom_vector) std::vector<PrepFileSpace::PrepFileAtom*>;
//std::vector<Dihedral> improper_dihedrals_;
%template(dihedral_vector) std::vector<std::vector<std::string> >;

////std::vector<Geometry::Coordinate*> coordinates_;
%template(coordinate_vector) std::vector<Geometry::Coordinate*>;

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

//typedef std::map<std::string, LibraryFileResidue*> ResidueMap;
%template() std::pair<std::string, LibraryFileSpace::LibraryFileResidue*>;
%template(residue_map_library_file) std::map<std::string, LibraryFileSpace::LibraryFileResidue*>;

//typedef std::map< std::string, PrepFileResidue* > ResidueMap;
%template() std::pair<std::string, PrepFileSpace::PrepFileResidue*>;
%template(residue_map_prep_file) std::map<std::string, PrepFileSpace::PrepFileResidue*>;

//typedef std::map<int, LibraryFileAtom*> AtomMap;
%template() std::pair<int, LibraryFileSpace::LibraryFileAtom*>;
%template(atom_map_library_file) std::map<int, LibraryFileSpace::LibraryFileAtom*>;

//typedef std::map<int, int> Loop;
%template() std::pair<int,int>;
%template(loop_map_prep_file) std::map<int, int>;

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












