import datetime
import subprocess
from . import key_and_values

def parse(file_path):
    SMAT_ENTRIES=[]
    with open(file_path,'r') as SMAT_FILE:
        line_count = 0
        for line in SMAT_FILE:
            line_count += 1
            if line_count > 1:
                SMAT_LINE_ENTRY = {}
                split_by_double_semicolon = line.split(';;')
                Label_Type_Status_Date_Ions_Energy = split_by_double_semicolon[0]
                Split_Label_Type_Status_Date_Ions_Energy = Label_Type_Status_Date_Ions_Energy.split(';')
                SMAT_LINE_ENTRY[key_and_values.LABEL_KEY] = Split_Label_Type_Status_Date_Ions_Energy[0].strip()
                SMAT_LINE_ENTRY[key_and_values.TYPE_KEY] = Split_Label_Type_Status_Date_Ions_Energy[1].strip()
                SMAT_LINE_ENTRY[key_and_values.STATUS_KEY] = Split_Label_Type_Status_Date_Ions_Energy[2].strip()
                SMAT_LINE_ENTRY[key_and_values.DATE_KEY] = Split_Label_Type_Status_Date_Ions_Energy[3].strip()
                SMAT_LINE_ENTRY[key_and_values.IONS_KEY] = Split_Label_Type_Status_Date_Ions_Energy[4].strip()
                SMAT_LINE_ENTRY[key_and_values.ENERGY_KEY] = Split_Label_Type_Status_Date_Ions_Energy[5].strip()

                RotamerList = split_by_double_semicolon[1]
                Split_RotamerList = RotamerList.split(';')
                Strip_Split_RotamerList = list(map (str.strip, Split_RotamerList))
                SMAT_LINE_ENTRY[key_and_values.ROTAMER_LIST_KEY] = Strip_Split_RotamerList
                SMAT_ENTRIES.append(SMAT_LINE_ENTRY)

    return SMAT_ENTRIES

def write_shadow_SMAT(SMAT_ENTRIES, file_path):
    max_length_per_column = [0, 0, 0, 0, 0, 0, 0]
    for entry in SMAT_ENTRIES:
        if len(entry[key_and_values.LABEL_KEY]) > max_length_per_column[0]:
            max_length_per_column[0] = len(entry[key_and_values.LABEL_KEY])
        if len(entry[key_and_values.TYPE_KEY]) > max_length_per_column[1]:
            max_length_per_column[1] = len(entry[key_and_values.TYPE_KEY])
        if len(entry[key_and_values.STATUS_KEY]) > max_length_per_column[2]:
            max_length_per_column[2] = len(entry[key_and_values.STATUS_KEY])
        if len(entry[key_and_values.DATE_KEY]) > max_length_per_column[3]:
            max_length_per_column[3] = len(entry[key_and_values.DATE_KEY])
        if len(entry[key_and_values.IONS_KEY]) > max_length_per_column[4]:
            max_length_per_column[4] = len(entry[key_and_values.IONS_KEY])
        if len(entry[key_and_values.ENERGY_KEY]) > max_length_per_column[5]:
            max_length_per_column[5] = len(entry[key_and_values.ENERGY_KEY])

        rotamer_list_str = ";".join(entry[key_and_values.ROTAMER_LIST_KEY])
        if len(rotamer_list_str) > max_length_per_column[6]:
            max_length_per_column[6] = len(rotamer_list_str)

    with open(file_path,'w+') as SHADOW_SMAT:
        SHADOW_SMAT.write("Label   ; Type      ; Status   ; Date       ; Ions ; Energy   ;; Rotamer List (link#, angle, rotamer)\n")
        for entry in SMAT_ENTRIES:
            rotamer_list_str1 = ";".join(entry[key_and_values.ROTAMER_LIST_KEY])
            rotamer_list_str1_formatted = rotamer_list_str1.center(max(37,max_length_per_column[6]), ' ')

            label_formatted = entry[key_and_values.LABEL_KEY].center(max(9,max_length_per_column[0]), ' ')
            type_formatted = entry[key_and_values.TYPE_KEY].center(max(12,max_length_per_column[1]), ' ')
            status_formatted = entry[key_and_values.STATUS_KEY].center(max(11,max_length_per_column[2]), ' ')
            date_formatted = entry[key_and_values.DATE_KEY].center(max(13,max_length_per_column[3]), ' ')
            ions_formatted = entry[key_and_values.IONS_KEY].center(max(7,max_length_per_column[4]), ' ')
            energy_formatted = entry[key_and_values.ENERGY_KEY].center(max(12,max_length_per_column[5]), ' ')
            line_formatted_str = label_formatted + ";" + type_formatted + ";" + status_formatted + ";" + date_formatted + ";" + ions_formatted + ";" + energy_formatted + ";;" + rotamer_list_str1_formatted + '\n'
            SHADOW_SMAT.write(line_formatted_str)

