library ieee;
	use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;

entity compteur_n is
    generic(C_NB_BIT_COUNTER : integer;
            C_MODULO : integer );
	port(
		clk 		: in	std_logic;
		rst 		: in	std_logic;
		enable 		: in	std_logic;
		max         : out std_logic ;
		out_count	: out	std_logic_vector (C_NB_BIT_COUNTER-1 downto 0)
	);
end compteur_n;

architecture behavioral of compteur_n is
	signal count : unsigned(C_NB_BIT_COUNTER-1 downto 0) := (others => '0');
begin
	compteur : process (clk)
	begin
		if rising_edge(clk) then
			if rst = '1' then -- reset synchrone
			    max <= '0' ;
				count <= (others => '0') ;
			elsif enable = '1' then
				if count = C_MODULO-1 then -- on compte de 0 à 9
				    max <= '1' ; -- le témoin de maximum sera actif après avoir atteint la valeur maximale
					count <= (others => '0'); -- on réinitialise le compteur à 0
				else
				    max <='0';
					count <= count + 1;
				end if ;
			end if ;
		end if ;
	end process;

	out_count <= std_logic_vector(count);

end behavioral;