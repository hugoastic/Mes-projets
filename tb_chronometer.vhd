library IEEE;
    use ieee.std_logic_1164.all;
	use ieee.numeric_std.all;


entity tb_chronometer is
end tb_chronometer;

architecture Behavioral of tb_chronometer is
    signal clk_tb		: std_logic	:='0';
	signal rst_tb		: std_logic	:='0';
	signal start_tb	: std_logic	:='0';
	signal seconds_tb     : std_logic_vector(7 downto 0) ;
	signal minutes_tb: std_logic_vector(7 downto 0)	;
begin
	inst : entity work.chronometer
		port map(
			clk			=> clk_tb,
			rst			=> rst_tb,
			start		=> start_tb,
			seconds     => seconds_tb,
			minutes	=> minutes_tb
		);
	
	clk_tb <= not clk_tb after 0.1 ns;	-- Periode : 0.2ns 

	stim_proc :	process
	begin
		rst_tb		<= '1';
		start_tb	<= '0';
		wait for 5 ns;

		rst_tb		<= '0';
		start_tb	<= '0';
		wait for 2 ns;

		rst_tb		<= '0';
		start_tb	<= '1';
		wait for 100000 ms;

		rst_tb		<= '0';
		start_tb	<= '0';
		wait for 2000 ms;


		wait;
    end process;
end Behavioral;
