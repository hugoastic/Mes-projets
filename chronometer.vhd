library IEEE;
	use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;

entity chronometer is
    port(
    clk : in STD_LOGIC;
    rst : in STD_LOGIC;
    start : in STD_LOGIC;
    seconds : out STD_LOGIC_VECTOR (7 downto 0);
    minutes : out STD_LOGIC_VECTOR (7 downto 0)
);
end chronometer;

architecture Behavioral of chronometer is
    constant nb_bit : integer := 27; --constante pour modifier la fréquence de la clock afin de voir des résultats lors de la simulation 
    constant modulo : integer := 100000000 ;
    signal max0 :  std_logic :='0' ;
    signal max1 :  std_logic :='0' ;
    signal max2 :  std_logic :='0' ;
    signal second_int : std_logic_vector(5 downto 0) :=(others=>'0'); -- création de vecteur de 6 bit pour se fier au compteur
    signal minute_int : std_logic_vector(5 downto 0) :=(others=>'0');

begin --3 instanciation de compteur modulo n 
     inst1 : entity work.compteur_n --le premier se cale sur la clock et permet d'avoir un max toutes les secondes 
         generic map(C_NB_BIT_COUNTER => nb_bit,
	                  C_MODULO => modulo)
		 port map(
			 clk		=> clk,
			 rst		=> rst,
			 enable		=> start,
			 max        => max0,
			 out_count	=> open
		);
     inst2 : entity work.compteur_n  --le second permet de modéliser les secondes 
	           generic map(C_NB_BIT_COUNTER => 6,
	                  C_MODULO => 60)
		       port map(
			     clk		=> clk,
			     rst		=> rst,
			     enable		=> max0,
			     max        => max1,
			     out_count	=> second_int
		);
	max2<= max1 and max0 ; 
	seconds <= "00" & second_int; --concaténation avec un vecteur de 2 bit pour avoir un vecteur de 8 bits comme dans l'énoncé
	inst3 : entity work.compteur_n --le dernier modélise les minutes 
		 generic map(C_NB_BIT_COUNTER => 6,
	                  C_MODULO => 60)
		 port map(
			 clk		=> clk,
			 rst		=> rst,
			 enable		=> max2,
			 max        => open,
			 out_count	=> minute_int
		);
		minutes <="00" & minute_int; --concaténation avec un vecteur de 2 bit pour avoir un vecteur de 8 bits comme dans l'énoncé
    
end Behavioral;
