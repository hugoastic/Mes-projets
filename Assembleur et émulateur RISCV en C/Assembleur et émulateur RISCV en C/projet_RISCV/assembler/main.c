#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/*Déclaration des variables globales et des structures*/

/* on crée un dictionnaire pour avoir, selon l'opcode, le format de l'instruction finale en binaire*/
typedef struct {
  char *instruction;
  char *format;
  uint32_t opcodebin;
  uint32_t funct3;
  uint32_t funct7;
}format_instruction;

format_instruction opcode_table[13] = {
        {"add","R",0b0110011,0x0, 0x00},
        {"sub","R",0b0110011, 0x0, 0x20},
        {"addi","I",0b0010011, 0x0, 0x9},
        {"ld" ,"I", 0b0000011 ,0x3 ,0x9},
        {"sd", "S" ,0b0100011,0x3,0x9},
        {"beq", "B" ,0b1100011, 0x0,0x9},
        {"bne" , "B", 0b1100011, 0x1,0x9 },
        {"blt" , "B" ,0b1100011, 0x4, 0x9 },
        {"bge" , "B", 0b1100011, 0x5,0x9},
        {"jal", "J", 0b1101111,0x9,0x9}, 
        {"j", "J", 0b1101111,0x9,0x9}, 
        {"li", "I", 0b0010011, 0x0, 0x9}, 
        {"mv", "I", 0b0010011, 0x0, 0x9}, 
        /* on a le nom de l'opcode, le type d'instruction, son format binaire, le funct3 et le funct7 */
        /* on rajoute aussi les cas particuliers*/
      };
/* REMARQUE: le 0x9 remplace la valeur NULL étant donnée qu'elle n'existe pas en uint_32*/

/* Notre programme doit reconnaitre les 2 noms différentes pour chaque registre*/
const char *registres_tab[] = {"zero", "ra", "sp",  "gp",  "tp", "t0", "t1", "t2",
                                  "s0",   "s1", "a0",  "a1",  "a2", "a3", "a4", "a5",
                                  "a6",   "a7", "s2",  "s3",  "s4", "s5", "s6", "s7",
                                  "s8",   "s9", "s10", "s11", "t3", "t4", "t5", "t6"}; 
                                  /* pour trouver la correspondance avec ce que comprend le Risc V on prend l'indice du tableau et on rajoute x devant pour zero on x0*/
const char *registres_x[] = {"x0", "x1", "x2",  "x3",  "x4", "x5", "x6", "x7",
                                  "x8",   "x9", "x10",  "x11",  "x12", "x13", "x14", "x15",
                                  "x16",   "x17", "x18",  "x19",  "x20", "x21", "x22", "x23",
                                  "x24",   "x25", "x26", "x27", "x28", "x29", "x30", "x31"}; 
       




/* Déclaration des fonctions secondaires à notre programme principal*/


/*fonction pour rechercher dans notre structure, la bonne liste correspondant à l'opcode en entrée de la fonction, contenant le format et différentes infos pour l'instruction finale*/
format_instruction rechercheopc(char* code){
  /*Traitement des cas généraux*/
  int exist=0;
  format_instruction resultat;
  for (int indice=0 ; indice<13 ; indice++){
    if (strcmp(code, opcode_table[indice].instruction)==0){
      resultat=opcode_table[indice];
      exist=1;
    }
  }
  if (exist==0){/*si l'opcode n'existe pas, on arrête le programme et on retourne un message d'erreur*/
        printf("The opcode : %s doesn't exist -- END PROGRAM\n",code);
        exit(EXIT_FAILURE);
  }
  else{
    return(resultat);
  }
}


/*fonction pour construire notre instruction selon l'opcode et les registres*/
uint32_t instruction_sequence(format_instruction opcode_inst , char registre[6][6], int v_imm){ 

  uint32_t sequence=0b00000000000000000000000000000000;
  int val;
  
  /*Type R*/
  if (strcmp(opcode_inst.format,"R")==0){
    /*funct 7*/
    sequence=sequence | opcode_inst.funct7;
    
    /*rs2*/
    sequence=sequence<<5;
    val=atoi(registre[2]);
    sequence= sequence | val;
    
    /*rs1*/
    sequence=sequence<<5;
    val=atoi(registre[1]);
    sequence=sequence | val;
    
    /*funct3*/
    sequence=sequence<<3;
    sequence=sequence | opcode_inst.funct3;
    
    /*rd*/
    sequence=sequence<<5;
    val=atoi(registre[0]);
    sequence=sequence | val;
    
    /*opcode*/
    sequence=sequence<<7;
    sequence=sequence | opcode_inst.opcodebin;
  }
  
  /*Type I*/
  if (strcmp(opcode_inst.format,"I")==0){            
    /*imm[11:0]*/
    if(strcmp(opcode_inst.instruction,"mv")==0){/*Cas particulier*/
      sequence=sequence | 0b000000000000;
    }
    else{
      sequence=sequence | v_imm;
    }

    /*rs1*/
    sequence=sequence<<5;
    if (strcmp(opcode_inst.instruction,"li")==0){/*Cas particulier*/
      val=0;
    }
    else{
      val=atoi(registre[1]);
    }
    sequence=sequence | val;
    
    /*funct3*/
    sequence=sequence<<3;
    sequence=sequence | opcode_inst.funct3;
    
    /*rd*/
    sequence=sequence<<5;
    val=atoi(registre[0]);
    sequence=sequence | val;
    
    /*opcode*/
    sequence=sequence<<7;
    sequence=sequence | opcode_inst.opcodebin;
  }
  
  /*Type S*/
  if (strcmp(opcode_inst.format,"S")==0){
    /*imm[11;5]*/
    uint32_t bin1=0b111111100000;
    uint32_t vim=v_imm & bin1;
    vim=vim>>5;
    sequence=sequence | vim;
    
    /*rd*/
    sequence=sequence<<5;
    val=atoi(registre[0]);
    sequence=sequence | val;
    
    /*rs1*/
    sequence=sequence<<5;
    val=atoi(registre[1]);
    sequence=sequence | val;
    
    /*funct3*/
    sequence=sequence<<3;
    sequence=sequence | opcode_inst.funct3;
    
    /*imm[4;0]*/
    sequence=sequence<<5;
    uint32_t bin2=0b000000011111;
    vim=v_imm & bin2;
    sequence=sequence | vim;
    
    /*opcode*/
    sequence=sequence<<7;
    sequence=sequence | opcode_inst.opcodebin;
    
  }
  /*Type B*/
  if (strcmp(opcode_inst.format,"B")==0){
    /*imm*[12|10:5]*/
    uint32_t bin1=0b0011111100000;
    uint32_t bin12=0b1000000000000;
    uint32_t vim1= v_imm & bin12;
    uint32_t vim2=v_imm & bin1;
    vim2=vim2 >> 5;
    vim1=vim1 >>6;
    vim1=vim1 | vim2;
    sequence=sequence | vim1;
    
    /*rs2*/
    sequence=sequence<<5;
    val=atoi(registre[1]);
    sequence=sequence | val;
    
    /*rs1*/
    sequence=sequence<<5;
    val=atoi(registre[0]);
    sequence=sequence | val;
    
    /*funct3*/
    sequence=sequence<<3;
    sequence=sequence | opcode_inst.funct3;
    
    /*imm[4:1|11]*/
    sequence=sequence<<5;
    bin1=0b0000000011110;
    uint32_t bin11=0b0100000000000;
    vim1= v_imm & bin1;
    vim2=v_imm & bin11;
    vim2 = vim2 >> 11;
    vim1=vim1 | vim2;
    sequence=sequence | vim1;
    
    /*opcode*/
    sequence= sequence<<7;
    sequence=sequence | opcode_inst.opcodebin;
  }
  /*Type J*/
  if (strcmp(opcode_inst.format,"J")==0){
    /*imm[20| 10:1 | 11 | 19:12]*/
    uint32_t bin20= 0b100000000000000000000;
    uint32_t bin11= 0b000000000100000000000;
    uint32_t bin1to10= 0b000000000011111111110;
    uint32_t bin12to19= 0b011111111000000000000;
    uint32_t vim1=v_imm & bin20;
    uint32_t vim2=v_imm & bin11;
    uint32_t vim3 =v_imm & bin1to10;
    uint32_t vim4 = v_imm & bin12to19;
    vim1=vim1>>1;
    vim4=vim4 >>12;
    vim2=vim2>>3;
    vim4 = vim4 | vim2;
    vim3 = vim3 <<8;
    vim4=vim4| vim3;

    vim4=vim4 | vim1;

    sequence=sequence | vim4;
    
    /*rd*/
    sequence=sequence<<5;
    if (strcmp(opcode_inst.instruction,"j")==0){
      val=0b00000;
    }
    else{
    val=atoi(registre[0]);
    }
    sequence=sequence | val;
    
    /*opcode*/
    sequence=sequence<<7;
    sequence=sequence | opcode_inst.opcodebin;

  }
  
  return(sequence);
}






/*Programme principal*/

int main(int argc, char **argv)
{
    /* ./riscv-assembler <ASSEMBLER INPUT> <HEX OUTPUT> */
    if(argc != 3) {
        printf("usage: ./riscv-assembler <ASSEMBLER INPUT> <HEX OUTPUT>\n");
        return 1;
    }

    char *asm_input_file = argv[1];
    char *hex_output_file = argv[2];
    FILE *fichier_s = fopen(asm_input_file,"r");
    FILE *fichier_hex = fopen(hex_output_file,"w");
    
    
    /*Lecture fichier ligne par ligne*/
    char *ligne = NULL;
    size_t len = 0;
    
    if (fichier_s == NULL){/* gestion d'erreur si le fichier est mal renseigné*/
        printf("Files provided unavailable or wrong directory\n");
        exit(EXIT_FAILURE);
    }
    
    /* Etape 1: On s'occupe d'écrire chaque ligne dans une chaine de caractères en ignorant les virgules, parenthèses et #*/
    while ((getline(&ligne, &len, fichier_s)) != -1) { 
      char ligneCourante[25]=""; 
      
      
      if ((ligne[0]!='#') && (ligne[0]!='\n') && (ligne[0]!=' ')){ /*On ne s'occupe pas, pour la suite de notre programme, des lignes commencant par # ou par des sauts de lignes*/
      
      
        int j=0;
        for (int i=0 ;(ligne[i]!='\0') && (ligne[i]!='\n') && (ligne[i]!=')');++i){
        
          if ((ligne[i]=='(') || (ligne[i]==',')){ /*on ne veut pas récupérer les virgules et parenthèses*/
            if (ligne[i+1]!=' '){ 
              ligneCourante[j]=' ';
              ++j;
            }
            else{
              ligneCourante[j]=' ';/*si un espace est déja présent après la virgule on incrémente i de un en plus de l'incrémentation normale */
              ++i;
              ++j;
            }
          }
          
          else{
            ligneCourante[j]=ligne[i];
            ++j;
          }
        }        
      
      
        /* Etape 2: On va maintenant traiter séparément, en s'occupant toujours d'une ligne à la fois, l'opcode et les registres utilisés selon le type d'opcode*/
        char *separation=" ";
        char *reg_opc_sep = strtok(ligneCourante, separation);
        int nbr_reg=32;
        int v_imm=0;
        char registre[6][6]={};
        int indice=0;
        format_instruction opc;
      
        for (int numero_mot=0;  (reg_opc_sep != NULL) ; ++numero_mot) {/*affichage de chaque élément de la ligne séparé par un espace*/
      
          /*on traite l'opcode*/
          if (numero_mot==0){
            opc =rechercheopc(reg_opc_sep);/* on retourne notre dictionnaire que l'on nomme opc correspondant à l'opcode de la ligne*/
          }
        
         /* on traite les registres ou les valeurs immédiates*/
        
          else{
          
            /*si notre sous-chaine de caractère commence par un signe négatif ou un chiffre entre 0 et 9 c'est une valeur immédiate*/
            if ( (reg_opc_sep[0]=='-') ||( (reg_opc_sep[0]>='0') && (reg_opc_sep[0]<='9') ) ) { /* cas des valeurs immédiates*/
              v_imm=atoi(reg_opc_sep);/*fonction pour convertir char en int*/
            }
            /*sinon c'est un opcode*/
            else{
              for (int reg=0 ; reg<nbr_reg ; ++reg){ 
              /* on veut que notre programme reconnaisse les deux noms possibles pour chaque registre*/
                if ((strcmp(reg_opc_sep,registres_tab[reg])==0) || (strcmp(reg_opc_sep,registres_x[reg])==0)){
                  sprintf(registre[indice], "%d", reg);/*on récupère les registres et on les transforme en type x0 à x31 et on prend que la valeur entre 0 et 31*/
                  ++indice;
                }
              }
            }
            
          }  
        /*on passe à la sous-chaine de caractères suivante*/
        reg_opc_sep = strtok(NULL, separation); 
        }
        
        /*Etape3: on utilise la fonction instruction_sequence pour retourner notre ligne de 32 bits correspondant à l'opcode et les registres indiqués dans la ligne en cours*/
        uint32_t instruction_ligne= instruction_sequence(opc, registre, v_imm);
        fprintf(fichier_hex,"%08x\n",instruction_ligne);
        printf("%08x\n",instruction_ligne);
      }
      
    }
    
    free(ligne);
  
    fclose(fichier_hex);
    fclose(fichier_s);
    
    return 0;
}
