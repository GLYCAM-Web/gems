#include<fstream>
#include<string>
#include<iostream>
#include<sstream>

int main(int argc, char* argv[]){
    std::string line;
    for (unsigned int i = 1 ; i < argc; i++){
	std::string argv_str = std::string(argv[i]);
        std::ifstream read_pdb(argv_str);
	std::string outgoing_path = "output_pdbs/";
	outgoing_path += argv_str;
	std::ofstream write_pdb(outgoing_path);

	int atom_line_count = 0;
	while(std::getline(read_pdb, line)){

	    if (line.find("HETATM") == std::string::npos){
	        write_pdb << line << std::endl;
	    }
	    else{
		atom_line_count++;
	        std::string untouched_part = line.substr(17);
		//std::cout << "Untouched part: " << untouched_part << std::endl;
	        std::string touched_part = line.substr(0,17);
		//std::cout << "Touched part: " << touched_part << std::endl;
                std::stringstream int_str_converter;

		if (touched_part.substr(12,1) == " "){
		    //std::cout << "Erase" << std::endl;
		    touched_part.erase(12,1);
		}

		while(true){
		    if (touched_part.substr(touched_part.size()-1) == " "){
		        touched_part.erase(touched_part.size()-1,1);
		    }
		    else{
		        break;
		    }
		}

		int_str_converter << atom_line_count;
		std::string atom_number_str = int_str_converter.str();
		touched_part += atom_number_str;

		//std::cout << "Touched part: " << touched_part << " size: " << touched_part.size() << std::endl;
		int num_spaces_to_append = 17 - touched_part.size();
		for (unsigned int i = 0; i < num_spaces_to_append; i++){
		    touched_part+=" ";
		}
		//std::cout << "New size: " << touched_part.size() << std::endl;
		write_pdb << touched_part << untouched_part << std::endl;
		
	    }
	}

	read_pdb.close();
	write_pdb.close();
    }
}
