#!/usr/bin/env python
import os
import sys
import subprocess

import argparse

import random

import string
import csv

import pandas as pd
import numpy as np


def concatenate_dataframes_with_padding(dfs):
    """
    Concatenate a list of dataframes vertically, ensuring that all dataframes have the same number of rows.
    If a dataframe has fewer rows, it is padded with NaNs.

    :param dfs: List of pandas DataFrames to concatenate
    :return: Concatenated DataFrame
    """
    # Determine the maximum number of rows in any of the dataframes
    max_rows = max(df.shape[0] for df in dfs)

    # Function to pad dataframe with NaNs to match the max number of rows
    def pad_df(df):
        rows_to_add = max_rows - df.shape[0]
        if rows_to_add > 0:
            # Create a DataFrame of NaNs with the required number of rows and columns
            padding_df = pd.DataFrame(np.nan, index=range(rows_to_add), columns=df.columns)
            # Append the padding DataFrame to the original DataFrame
            return df.append(padding_df, ignore_index=True)
        else:
            return df

    # Pad each dataframe and concatenate them
    padded_dfs = [pad_df(df) for df in dfs]
    concatenated_df = pd.concat(padded_dfs, axis=1)

    return concatenated_df

# defining colors for print to make debugs and .log files readable
green_color = "\033[32m"
blue_color = "\033[34m"
red_color= "\033[31m"
yellow_color = "\033[33m"
# Reset ANSI escape code to default color
reset_color = "\033[0m"



# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root) of the current directory
project_root = os.path.dirname(current_dir)

# Add the project root directory to PYTHONPATH
sys.path.append(project_root)

# Global varible, drug names:

# Drug_number, orders 
drug_names=["Amikacin",
            "Bedaquiline",
            "Clofazimine",
            "Delamanid",
            "Ethambutol",
            "Ethionamide",
            "Isoniazid",
            "Kanamycin",
            "Levofloxacin",
            "Linezolid",
            "Moxifloxacin",
            "Rifampicin",
            "Rifabutin",
            "RIA",
            "AMG",
            "FQS"]


#                                   Drug number
# drug_names=["Amikacin",\              0       
#             "Bedaquiline",\           1
#             "Clofazimine",\           2
#             "Delamanid",\             3
#             "Ethambutol",\            4
#             "Ethionamide",\           5
#             "Isoniazid",\             6
#             "Kanamycin",\             7
#             "Levofloxacin",\          8
#             "Linezolid",\             9
#             "Moxifloxacin",\          10
#             "Rifampicin",\            11
#             "Rifabutin",\             12
#             "RIA",\                   13
#             "AMG",\                   14
#             "FQS"]                    15


def line_parser (string):
    count = string.count("(")
    first_paranthesis_index = string.find("(")
    
    kmer_index=int(string[0:first_paranthesis_index-1]) # This is index of the kmer which is at the end of each array _ the size will be 6225, in which the first 6224 ones are the mains and the last is kmer index
    return count, kmer_index


def main():
    # Parsing input arguments:
    valid_fasta_extensions = ["fasta", "fa", "fas", "fna", "ffn"]
    parser = argparse.ArgumentParser(
        description=f"{green_color}Required options{reset_color}:\n"
                f"-{green_color}i {reset_color}-{green_color}I{reset_color} Input resistant_genome_IDs.csv, the header of the CSV file should be the antibiotics (Amikacin, ....)\n"
                f"-{green_color}o {reset_color}-{green_color}O{reset_color} The output file which will be .csv (required)\n"
                f"-{green_color}b {reset_color}-{green_color}B{reset_color} The directory including the FASTA files (required)\n"
                f"-{green_color}f {reset_color} The extensions of the Fasta files\nThe valid FASTA extensions are: {green_color}{valid_fasta_extensions}{reset_color}\n"
                f"-{green_color}t {reset_color},--{green_color}temporary-directory{reset_color} This is a directory of Temporary files. Depending on the number of Genomes to be Processed, the free space to increase \n"
                ,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    usage='%(prog)s -i PATH/resistant_genome_IDs -o PATH/output.csv -b Base_directory_of_FASTA_File -f FASTA_extention\n'  # Custom usage line
    )

    parser.add_argument("-i", "--I", type=str, required=True)
    parser.add_argument("-o", "--O", type=str, required=True)
    parser.add_argument("-b", "--B", type=str, required=True)
    parser.add_argument("-f", type=str, required=True)
    parser.add_argument("-t", "--temporary-directory", type=str, required=True)

    args = parser.parse_args()

    FASTA_extention= args.f
    # Check if the output file path is an absolute path or a relative path
    if not os.path.isabs(args.O):
        # Construct the absolute path for the output file based on the current working directory
        output_file_address = os.path.abspath(args.O)
    else:
        output_file_address = args.O

    if not os.path.isabs(args.B):
        # Construct the absolute path for the output file based on the current working directory
        base_directory = os.path.abspath(args.B)
    else:
        base_directory = args.B

    if not os.path.isdir(args.temporary_directory):
        print(f"{red_color}Error: The directory '{args.temporary_directory}' does not exist.{reset_color}")
        print(f"{red_color}Aborted!{reset_color}")
        sys.exit(1)

    temp_dir=args.temporary_directory


    genome_id_csv_file = args.I

    # Read the CSV file using pandas
    genome_id_df = pd.read_csv(genome_id_csv_file)


    


    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits
    
    
    # Generate a random 20-character string to be used as the name for temporary files during the processing
    prefix_temporary_files =''.join(random.choice(characters) for _ in range(25))
    prefix_temporary_files =''.join("2PIn9iqosr6LyveTjUYDf4STC")
    #Calculating the color matrix and parsing 
    #the Ascii code and doing the classification 
    #at the same time
    

    #These lists contain the information that will further be reported
    dfs = []
    output_dataframe=pd.DataFrame()
    for drug in drug_names:

        #Address to the SBWK index for each specific drug
        #SBWT_index = os.path.join(current_dir, "data", "SBWT_indexes","{}.sbwt".format(drug))
        SBWT_index = os.path.join(project_root,"MTB-plus-plus","data", "SBWT_indexes","{}.sbwt".format(drug))
        
        #Temporary random file names that will be removed later on
        #temporary_file=current_dir+"/temp/"+prefix_temporary_files+"_"+drug+".txt"
        temporary_kmer_list_file = os.path.join(temp_dir, prefix_temporary_files+"_31mers_"+drug+".txt")

        #Address to the dump_kmers
        address_to_dump_kmers= os.path.join(project_root,"MTB-plus-plus",'src',"SBWT-kmer-counters","dump_kmers") 

        command= address_to_dump_kmers+ " "+ SBWT_index + " > "+temporary_kmer_list_file

        #Runing the SBWT Kmer_dump to extract the top kmers for each antibiotic 
        try:
            subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{green_color}SBWT dump_kmers was successfully run for {drug}{reset_color}")
        except subprocess.CalledProcessError as e:
            error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
            print(f"{red_color}{error_message}{reset_color}")
            os.remove(temporary_kmer_list_file)
            raise  
        
        with open(temporary_kmer_list_file, "r") as file:
            text_content = file.read()

        pairs_list = [[line.strip(), 0] for line in text_content.split('\n')]
    


        # 
        temporary_genome_list_file = os.path.join(temp_dir, prefix_temporary_files+"_genome_list_"+drug+".txt")

        drug_column = genome_id_df[drug]
        #dropin Nans
        drug_column = drug_column.dropna()
        


        
        # Checking if the number of genome IDs are not zero since SBWT will crush if no genome IDs are present in it
        if len(drug_column) == 0:
            print(f"{yellow_color}There are ZERO genome IDs for {drug} {reset_color}")
            mid_df=pd.DataFrame([["_","0 genome IDs exist"]], columns=['{} top 31-mer'.format(drug),\
                                                '{} Kmer occurance (out of {}) '.format(drug,len(drug_column))])
            dfs.append(mid_df)
        else: # RUN SBWT multi genome color matrix
            # creating the list 
            absolute_addresses = [os.path.join(base_directory, str(genome_id)+"."+FASTA_extention) for genome_id in drug_column]
            # Write the absolute addresses to the output text file
            with open(temporary_genome_list_file, "w") as outfile:
                outfile.write("\n".join(absolute_addresses))
            
            temporary_color_matrix_file = os.path.join(temp_dir, prefix_temporary_files+"_multi_genome_color_matrix_"+drug+".txt")

            address_to_multi_genome_counters= os.path.join(project_root,"MTB-plus-plus",'src',"SBWT-kmer-counters","multi_genome_counters") 

            command= address_to_multi_genome_counters+ " "+ SBWT_index + " "+ temporary_genome_list_file + " > "+temporary_color_matrix_file

            try:
#################result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                #For devug purpose
                print(f"{green_color}SBWT multi_genome_counters was successfully run for {drug} for {reset_color}")
            except subprocess.CalledProcessError as e:
                error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
                print(f"{red_color}{error_message}{reset_color}")
                os.remove(temporary_kmer_list_file)
                raise  

            color_matrix_file = open(temporary_color_matrix_file,"r")
            
            for line in color_matrix_file:
                orrucance, _31_mer_index= line_parser(line)
                pairs_list[_31_mer_index][1]=orrucance
            
            pairs_list = [pair for pair in pairs_list if ("$" not in pair[0] and len(pair[0])!=0)]
            sorted_list = sorted(pairs_list, key=lambda x: x[1],reverse=True)

            mid_df=pd.DataFrame(sorted_list, columns=['{} top 31-mer'.format(drug),\
                                                '{} Kmer occurance (out of {})'.format(drug,len(drug_column))])
            dfs.append(mid_df) 

    output_dataframe = concatenate_dataframes_with_padding(dfs)  
    output_dataframe.to_csv("output_sorted.csv",index=False)

    

    
        
        


        
if __name__ == "__main__":
    main()
