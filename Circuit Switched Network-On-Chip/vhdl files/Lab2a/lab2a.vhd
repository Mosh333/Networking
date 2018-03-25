library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;



entity lab2a is
		generic (W: integer := 8);
		port(	in0, in1, in2, in3, in4: in STD_LOGIC_VECTOR(W-1 downto 0);
		adrPort: in STD_LOGIC_VECTOR(1 downto 0);
		clock, clear:			 in  std_logic;
		out0r, out1r, out2r, out3r, out4r : out STD_LOGIC_VECTOR(W-1 downto 0)
		);
end entity lab2a;

architecture routerNode of lab2a is  

signal in0r, in1r, in2r, in3r, in4r :  STD_LOGIC_VECTOR(W-1 downto 0);
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
	
	
	
	Latch0: process (in0, clock,clear) begin 
		if (clear = '1') then 
			for i in 0 to W-1 loop
				in0r(i) <= '0';
				-- in0r is the ‘registered’ or ‘latched’ version of in0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			in0r <= in0;
		end if;
	end process;
	
	LATCH1:  process (in1, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in1r(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in1r <= in1;
		end if;
	end process;

	LATCH2:  process (in2, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in2r(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in2r <= in2;
		end if;
	end process;
	
	LATCH3:  process (in3, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in3r(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in3r <= in3;
		end if;
	end process;
	
	LATCH4:  process (in4, clock, clear) begin
		if clear = '1' then
			for i in 0 to W-1 loop
				in4r(i) <= '0';
			end loop;
		elsif clock'EVENT and clock = '1' then
			in4r <= in4;
		end if;
	end process;
	--------------------------------------------------------
	my_MUX0: process(in0r, in1r, in2r, in3r,in4r,sel(2 downto 0)) --sel0
	begin
		case sel(2 downto 0) is 
			when "000" => out0 <= in0r;
			when "001" => out0 <= in1r;
			when "010" => out0 <= in2r;
			when "011" => out0 <= in3r;
			when "100" => out0 <= in4r;
			when others => null;
		end case;
	end process;
	
	my_MUX1: process(in0r, in1r, in2r, in3r,in4r,sel(5 downto 3)) --sel1
	begin
		case sel(5 downto 3) is 
			when "000" => out1 <= in0r;
			when "001" => out1 <= in1r;
			when "010" => out1 <= in2r;
			when "011" => out1 <= in3r;
			when "100" => out1 <= in4r;
			when others => null;
		end case;
	end process;
	
	my_MUX2: process(in0r, in1r, in2r, in3r,in4r,sel(8 downto 6)) --sel2
	begin
		case sel(8 downto 6) is 
			when "000" => out2 <= in0r;
			when "001" => out2 <= in1r;
			when "010" => out2 <= in2r;
			when "011" => out2 <= in3r;
			when "100" => out2 <= in4r;
			when others => null;
		end case;
	end process;
	
	my_MUX3: process(in0r, in1r, in2r, in3r,in4r,sel(11 downto 9)) --sel3
	begin
		case sel(11 downto 9) is 

			when "000" => out3 <= in0r;
			when "001" => out3 <= in1r;
			when "010" => out3 <= in2r;
			when "011" => out3 <= in3r;
			when "100" => out3 <= in4r;
			when others => null;
		end case;
	end process;
	
	my_MUX4: process(in0r, in1r, in2r, in3r,in4r, sel(14 downto 12)) --sel4
	begin
		case sel(14 downto 12) is 
			when "000" => out4 <= in0r;
			when "001" => out4 <= in1r;
			when "010" => out4 <= in2r;
			when "011" => out4 <= in3r;
			when "100" => out4 <= in4r;
			when others => null;
		end case;
	end process;
	--------------------------------------------------------
	stage2_Latch0: process (out0, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out0r(i) <= '0';
				-- out0r is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out0r <= out0;
		end if;
	end process;
		
	stage2_Latch1: process (out1, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out1r(i) <= '0';
				-- out0r is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out1r <= out1;
		end if;
	end process;
		
	stage2_Latch2: process (out2, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out2r(i) <= '0';
				-- out0r is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out2r <= out2;
		end if;
	 end process;
		
	stage2_Latch3: process (out3, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out3r(i) <= '0';
				-- out0r is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out3r <= out3;
		end if;
	 end process;
	
	 stage2_Latch4: process (out4, clock,clear) begin
	 if (clear = '1') then 
			for i in 0 to W-1 loop
				out4r(i) <= '0';
				-- out0r is the ‘registered’ or ‘latched’ version of out0
			end loop;
		elsif (clock'EVENT and clock = '1') then
			out4r <= out4;
		end if;
	 end process;
	
end architecture routerNode;