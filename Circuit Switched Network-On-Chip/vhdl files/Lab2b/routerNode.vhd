library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;



entity routerNode is
		generic (W: integer := 8);
		port(	in_N, in_E, in_S, in_W, in_D: in STD_LOGIC_VECTOR(W-1 downto 0);
		adrPort: in STD_LOGIC_VECTOR(1 downto 0);
		clock, clear:			 in  std_logic;
		out_N, out_E, out_S, out_W, out_D : out STD_LOGIC_VECTOR(W-1 downto 0)
		);
end entity routerNode;

architecture routerNode1 of routerNode is  

signal in_Nr, in_Er, in_Sr, in_Wr, in_Dr :  STD_LOGIC_VECTOR(W-1 downto 0);
signal out0, out1, out2, out3, out4:   STD_LOGIC_VECTOR(W-1 downto 0);

component LUT is --include object LUT
		port( address: in STD_LOGIC_VECTOR(1 downto 0);
				sel_LUT0,sel_LUT1,sel_LUT2,sel_LUT3,sel_LUT4: out STD_LOGIC_VECTOR(2 downto 0)
		);
end component;


signal sel: STD_LOGIC_VECTOR(14 downto 0);


begin 
	--map the output from LUT to signal in switch
	assign_LUT_switch: LUT port map(sel_LUT0 => sel(2 downto 0), sel_LUT1 => sel(5 downto 3),
	sel_LUT2 => sel(8 downto 6), sel_LUT3 => sel(11 downto 9),sel_LUT4 => sel(14 downto 12), address => adrPort);
	
	
	Latch0: process (in_N, clock,clear) begin 
		if (clear = '1') then 
			for i in 0 to W-1 loop
				in_Nr(i) <= '0';
				-- in_Nr is the ‘registered’ or ‘latched’ version of in_N
			end loop;
		elsif (clock'EVENT and clock = '1') then
			in_Nr <= in_N;
		end if;
	end process;
	
	LATCH1:  process (in_E, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in_Er(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in_Er <= in_E;
		end if;
	end process;

	LATCH2:  process (in_S, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in_Sr(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in_Sr <= in_S;
		end if;
	end process;
	
	LATCH3:  process (in_W, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in_Wr(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in_Wr <= in_W;
		end if;
	end process;
	
	LATCH4:  process (in_D, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in_Dr(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in_Dr <= in_D;
		end if;
	end process;
	--------------------------------------------------------
	my_MUX0: process(in_Nr, in_Er, in_Sr, in_Wr,in_Dr,sel(2 downto 0)) --sel0
	begin
		case sel(2 downto 0) is 
			when "000" => out0 <= in_Nr;
			when "001" => out0 <= in_Er;
			when "010" => out0 <= in_Sr;
			when "011" => out0 <= in_Wr;
			when "100" => out0 <= in_Dr;
			when others => null;
		end case;
	end process;
	
	my_MUX1: process(in_Nr, in_Er, in_Sr, in_Wr,in_Dr,sel(5 downto 3)) --sel1
	begin
		case sel(5 downto 3) is 
			when "000" => out1 <= in_Nr;
			when "001" => out1 <= in_Er;
			when "010" => out1 <= in_Sr;
			when "011" => out1 <= in_Wr;
			when "100" => out1 <= in_Dr;
			when others => null;
		end case;
	end process;
	
	my_MUX2: process(in_Nr, in_Er, in_Sr, in_Wr,in_Dr,sel(8 downto 6)) --sel2
	begin
		case sel(8 downto 6) is 
			when "000" => out2 <= in_Nr;
			when "001" => out2 <= in_Er;
			when "010" => out2 <= in_Sr;
			when "011" => out2 <= in_Wr;
			when "100" => out2 <= in_Dr;
			when others => null;
		end case;
	end process;
	
	my_MUX3: process(in_Nr, in_Er, in_Sr, in_Wr,in_Dr,sel(11 downto 9)) --sel3
	begin
		case sel(11 downto 9) is 

			when "000" => out3 <= in_Nr;
			when "001" => out3 <= in_Er;
			when "010" => out3 <= in_Sr;
			when "011" => out3 <= in_Wr;
			when "100" => out3 <= in_Dr;
			when others => null;
		end case;
	end process;
	
	my_MUX4: process(in_Nr, in_Er, in_Sr, in_Wr,in_Dr, sel(14 downto 12)) --sel4
	begin
		case sel(14 downto 12) is 
			when "000" => out4 <= in_Nr;
			when "001" => out4 <= in_Er;
			when "010" => out4 <= in_Sr;
			when "011" => out4 <= in_Wr;
			when "100" => out4 <= in_Dr;
			when others => null;
		end case;
	end process;
	--------------------------------------------------------
	stage2_Latch0: process (out0, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out_N(i) <= '0';
				-- out_N is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out_N <= out0;
		end if;
	end process;
		
	stage2_Latch1: process (out1, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out_E(i) <= '0';
				-- out_N is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out_E <= out1;
		end if;
	end process;
		
	stage2_Latch2: process (out2, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out_S(i) <= '0';
				-- out_N is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out_S <= out2;
		end if;
	 end process;
		
	stage2_Latch3: process (out3, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out_W(i) <= '0';
				-- out_N is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out_W <= out3;
		end if;
	 end process;
	
	 stage2_Latch4: process (out4, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out_D(i) <= '0';
				-- out_N is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out_D <= out4;
		end if;
	 end process;
	
end architecture routerNode1;