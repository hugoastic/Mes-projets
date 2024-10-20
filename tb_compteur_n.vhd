library ieee;
	use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;

entity tb_compteur_n is
end tb_compteur_n;

architecture behavioral of tb_compteur_n is
    constant C_NB_BIT_COUNTER : integer := 4 ;
    constant C_MODULO : integer := 10 ;
	signal clk_tb		: std_logic	:='0';
	signal rst_tb		: std_logic	:='0';
	signal enable_tb	: std_logic	:='0';
	signal max_tb       : std_logic ;
	signal out_count_tb	: std_logic_vector(C_NB_BIT_COUNTER-1 downto 0)	;
begin
	inst : entity work.compteur_n
	    generic map(C_NB_BIT_COUNTER => 4,
	               C_MODULO => 10)
		port map(
			clk			=> clk_tb,
			rst			=> rst_tb,
			enable		=> enable_tb,
			max         => max_tb,
			out_count	=> out_count_tb
		);
	
	clk_tb <= not clk_tb after 5 ns;	-- Periode : 10ns --> Frequence : 100MHz

	stim_proc :	process
	begin
		rst_tb		<= '1';
		enable_tb	<= '0';
		wait for 50 ns;

		rst_tb		<= '0';
		enable_tb	<= '0';
		wait for 20 ns;

		rst_tb		<= '0';
		enable_tb	<= '1';
		wait for 100 ns;

		rst_tb		<= '0';
		enable_tb	<= '0';
		wait for 20 ns;

		rst_tb		<= '0';
		enable_tb	<= '1';
		wait for 120 ns;

		rst_tb		<= '1';
		enable_tb 	<= '1';
		wait for 50 ns;

		rst_tb		<= '0';
		enable_tb 	<= '1';
		wait for 150 ns;

		wait;
    end process;
end behavioral;