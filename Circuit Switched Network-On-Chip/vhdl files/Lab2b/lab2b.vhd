
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;







entity lab2b is  --lab2b entity is the 16-Node Toroid
		generic (W: integer := 8);
		port(	Din0, Din1, Din2, Din3, Din4: in STD_LOGIC_VECTOR(W-1 downto 0);
		Din5, Din6, Din7, Din8, Din9: in STD_LOGIC_VECTOR(W-1 downto 0);
		Din10, Din11, Din12, Din13, Din14, Din15: in STD_LOGIC_VECTOR(W-1 downto 0);
		address_2b: in STD_LOGIC_VECTOR(1 downto 0);
		clock, clear:			 in  std_logic;
		Dout0, Dout1, Dout2, Dout3, Dout4: out STD_LOGIC_VECTOR(W-1 downto 0);
		Dout5, Dout6, Dout7, Dout8, Dout9: out STD_LOGIC_VECTOR(W-1 downto 0);
		Dout10, Dout11, Dout12, Dout13, Dout14, Dout15: out STD_LOGIC_VECTOR(W-1 downto 0)
		);
end entity lab2b;



architecture toroid of lab2b is  

component routerNode is
		generic (W: integer := 8);
		port(	in_N, in_E, in_S, in_W, in_D: in STD_LOGIC_VECTOR(W-1 downto 0);
		adrPort: in STD_LOGIC_VECTOR(1 downto 0);
		clock, clear:			 in  std_logic;
		out_N, out_E, out_S, out_W, out_D : out STD_LOGIC_VECTOR(W-1 downto 0)
		);
end component routerNode;

component routerNode_at_first_col is
		generic (W: integer := 8);
		port(	in_N, in_E, in_S, in_W, in_D: in STD_LOGIC_VECTOR(W-1 downto 0);
		adrPort: in STD_LOGIC_VECTOR(1 downto 0);
		clock, clear:			 in  std_logic;
		out_N, out_E, out_S, out_W, out_D : out STD_LOGIC_VECTOR(W-1 downto 0)
		);
end component routerNode_at_first_col;


signal nodein0_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein1_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein2_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein3_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein4_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein5_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein6_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein7_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein8_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein9_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein10_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein11_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein12_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein13_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein14_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein15_N: STD_LOGIC_VECTOR( 7 downto 0);

signal nodein0_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein1_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein2_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein3_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein4_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein5_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein6_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein7_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein8_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein9_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein10_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein11_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein12_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein13_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein14_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein15_E: STD_LOGIC_VECTOR( 7 downto 0);

signal nodein0_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein1_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein2_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein3_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein4_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein5_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein6_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein7_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein8_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein9_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein10_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein11_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein12_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein13_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein14_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein15_S: STD_LOGIC_VECTOR( 7 downto 0);

signal nodein0_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein1_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein2_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein3_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein4_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein5_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein6_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein7_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein8_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein9_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein10_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein11_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein12_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein13_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein14_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodein15_W: STD_LOGIC_VECTOR( 7 downto 0);

signal nodeout0_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout1_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout2_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout3_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout4_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout5_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout6_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout7_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout8_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout9_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout10_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout11_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout12_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout13_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout14_N: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout15_N: STD_LOGIC_VECTOR( 7 downto 0);

signal nodeout0_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout1_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout2_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout3_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout4_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout5_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout6_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout7_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout8_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout9_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout10_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout11_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout12_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout13_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout14_E: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout15_E: STD_LOGIC_VECTOR( 7 downto 0);

signal nodeout0_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout1_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout2_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout3_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout4_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout5_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout6_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout7_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout8_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout9_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout10_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout11_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout12_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout13_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout14_S: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout15_S: STD_LOGIC_VECTOR( 7 downto 0);

signal nodeout0_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout1_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout2_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout3_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout4_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout5_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout6_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout7_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout8_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout9_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout10_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout11_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout12_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout13_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout14_W: STD_LOGIC_VECTOR( 7 downto 0);
signal nodeout15_W: STD_LOGIC_VECTOR( 7 downto 0);

begin
	node0: routerNode_at_first_col port map (in_N => nodeout12_S, in_E => nodeout1_W, in_S => nodeout4_N, in_W => nodeout3_E,
											  out_N => nodeout0_N, out_E  => nodeout0_E, out_S  => nodeout0_S , out_W  => nodeout0_W,
											  in_D => Din0, out_D => Dout0, clock => clock, adrPort => address_2b, clear => clear
												);

	
	node1: routerNode port map (in_N => nodeout13_S, in_E => nodeout2_W, in_S => nodeout5_N, in_W => nodeout0_E,
											out_N => nodeout1_N, out_E  => nodeout1_E, out_S  => nodeout1_S , out_W  => nodeout1_W,
											in_D => Din1, out_D => Dout1, clock => clock, adrPort => address_2b, clear => clear
											);
											
	node2: routerNode port map (in_N => nodeout14_S, in_E => nodeout3_W, in_S => nodeout6_N, in_W => nodeout1_E,
											out_N => nodeout2_N, out_E  => nodeout2_E, out_S  => nodeout2_S , out_W  => nodeout2_W,
											in_D => Din2, out_D => Dout2, clock => clock, adrPort => address_2b, clear => clear
											);
											
	node3: routerNode port map (in_N => nodeout15_S, in_E => nodeout0_W, in_S => nodeout7_N, in_W => nodeout2_E,
											out_N => nodeout3_N, out_E  => nodeout3_E, out_S  => nodeout3_S , out_W  => nodeout3_W,
											in_D => Din3, out_D => Dout3, clock => clock, adrPort => address_2b, clear => clear
											);
											
	node4: routerNode_at_first_col port map (in_N => nodeout0_S, in_E => nodeout5_W, in_S => nodeout8_N, in_W => nodeout7_E,
											out_N => nodeout4_N, out_E  => nodeout4_E, out_S  => nodeout4_S , out_W  => nodeout4_W,
											in_D => Din4, out_D => Dout4, clock => clock, adrPort => address_2b, clear => clear
											);

	node5: routerNode port map (in_N => nodeout1_S, in_E => nodeout6_W, in_S => nodeout9_N, in_W => nodeout4_E,
											out_N => nodeout5_N, out_E  => nodeout5_E, out_S  => nodeout5_S , out_W  => nodeout5_W,
											in_D => Din5, out_D => Dout5, clock => clock, adrPort => address_2b, clear => clear
											);
		
	node6: routerNode port map (in_N => nodeout2_S, in_E => nodeout7_W, in_S => nodeout10_N, in_W => nodeout5_E,
											out_N => nodeout6_N, out_E  => nodeout6_E, out_S  => nodeout6_S , out_W  => nodeout6_W,
											in_D => Din6, out_D => Dout6, clock => clock, adrPort => address_2b, clear => clear
											);			

	node7: routerNode port map (in_N => nodeout3_S, in_E => nodeout4_W, in_S => nodeout11_N, in_W => nodeout6_E,
											out_N => nodeout7_N, out_E  => nodeout7_E, out_S  => nodeout7_S , out_W  => nodeout7_W,
											in_D => Din7, out_D => Dout7, clock => clock, adrPort => address_2b, clear => clear
											);		
											
	node8: routerNode_at_first_col port map (in_N => nodeout4_S, in_E => nodeout9_W, in_S => nodeout12_N, in_W => nodeout11_E,
											out_N => nodeout8_N, out_E  => nodeout8_E, out_S  => nodeout8_S , out_W  => nodeout8_W,
											in_D => Din8, out_D => Dout8, clock => clock, adrPort => address_2b, clear => clear
											);											
											
	node9: routerNode port map (in_N => nodeout5_S, in_E => nodeout10_W, in_S => nodeout13_N, in_W => nodeout8_E,
											out_N => nodeout9_N, out_E  => nodeout9_E, out_S  => nodeout9_S , out_W  => nodeout9_W,
											in_D => Din9, out_D => Dout9, clock => clock, adrPort => address_2b, clear => clear
											);											
											
	node10: routerNode port map (in_N => nodeout6_S, in_E => nodeout11_W, in_S => nodeout14_N, in_W => nodeout9_E,
											out_N => nodeout10_N, out_E  => nodeout10_E, out_S  => nodeout10_S , out_W  => nodeout10_W,
											in_D => Din10, out_D => Dout10, clock => clock, adrPort => address_2b, clear => clear
											);
											
	node11: routerNode port map (in_N => nodeout7_S, in_E => nodeout8_W, in_S => nodeout15_N, in_W => nodeout10_E,
											out_N => nodeout11_N, out_E  => nodeout11_E, out_S  => nodeout11_S , out_W  => nodeout11_W,
											in_D => Din11, out_D => Dout11, clock => clock, adrPort => address_2b, clear => clear
											);
											
	node12: routerNode_at_first_col port map (in_N => nodeout8_S, in_E => nodeout13_W, in_S => nodeout0_N, in_W => nodeout15_E,
											out_N => nodeout12_N, out_E  => nodeout12_E, out_S  => nodeout12_S , out_W  => nodeout12_W,
											in_D => Din12, out_D => Dout12, clock => clock, adrPort => address_2b, clear => clear
											);												
											
	node13: routerNode port map (in_N => nodeout9_S, in_E => nodeout14_W, in_S => nodeout1_N, in_W => nodeout12_E,
											out_N => nodeout13_N, out_E  => nodeout13_E, out_S  => nodeout13_S , out_W  => nodeout13_W,
											in_D => Din13, out_D => Dout13, clock => clock, adrPort => address_2b, clear => clear
											);		

	node14: routerNode port map (in_N => nodeout10_S, in_E => nodeout15_W, in_S => nodeout2_N, in_W => nodeout13_E,
											out_N => nodeout14_N, out_E  => nodeout14_E, out_S  => nodeout14_S , out_W  => nodeout14_W,
											in_D => Din14, out_D => Dout14, clock => clock, adrPort => address_2b, clear => clear
											);	
											
	node15: routerNode port map (in_N => nodeout11_S, in_E => nodeout12_W, in_S => nodeout3_N, in_W => nodeout14_E,
											out_N => nodeout15_N, out_E  => nodeout15_E, out_S  => nodeout15_S , out_W  => nodeout15_W,
											in_D => Din15, out_D => Dout15, clock => clock, adrPort => address_2b, clear => clear
											);											



end architecture toroid;
