
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std;

entity test_bench_2b is

end entity;

architecture test_behaviour of test_bench_2b is 

Shared variable endsim : boolean := FALSE;
Shared variable W : integer := 8;

--components
component lab2b is  --lab2b entity is the 16-Node Toroid
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
end component lab2b;

------------------------
--define signals below




--signal in_N_test, in_E_test, in_S_test, in_W_test, in_D_test: STD_LOGIC_VECTOR(W-1 downto 0);  --unsigned
--signal out_N_test, out_E_test, out_S_test, out_W_test, out_D_test: STD_LOGIC_VECTOR(W-1 downto 0);
signal Din0test, Din1test, Din2test, Din3test, Din4test, Din5test, Din6test, 
		Din7test, Din8test, Din9test, Din10test, Din11test, Din12test, Din13test, Din14test, Din15test: STD_LOGIC_VECTOR(W-1 downto 0);
		
signal Dout0test, Dout1test, Dout2test, Dout3test, Dout4test, Dout5test, Dout6test, Dout7test, Dout8test, Dout9test,
		Dout10test, Dout11test, Dout12test, Dout13test, Dout14test, Dout15test: STD_LOGIC_VECTOR(W-1 downto 0);
		
		

signal clock_test : STD_LOGIC;
signal clear_test: STD_LOGIC;
signal address_test: STD_LOGIC_VECTOR(1 downto 0);


begin


 -- Instantiate the Unit Under Test (UUT)
   uut: lab2b generic map(w) PORT MAP (            --double check which signals are to be kept
			clock=>clock_test, clear => clear_test,
--			in_N=>in_N_test, in_E=>in_E_test, in_S=>in_S_test, in_W=>in_W_test, in_D=>in_D_test,
--			out_N=>out_N_test, out_E=>out_E_test, out_S=>out_S_test, out_W=>out_W_test, out_D=>out_D_test,
			address_2b => address_test, Din0 => Din0test, Din1 => Din1test, Din2 => Din2test, Din3 => Din3test, Din4 => Din4test,
			Din5 => Din5test, Din6 => Din6test, Din7 => Din7test, Din8 => Din8test, Din9 => Din9test, Din10 => Din10test, Din11 => Din11test,
			Din12 => Din12test, Din13 => Din13test, Din14 => Din14test, Din15 => Din15test,
			 
			Dout0 => Dout0test, Dout1 => Dout1test, Dout2 => Dout2test, Dout3 => Dout3test, Dout4 => Dout4test,
			Dout5 => Dout5test, Dout6 => Dout6test, Dout7 => Dout7test, Dout8 => Dout8test, Dout9 => Dout9test, Dout10 => Dout10test, Dout11 => Dout11test,
			Dout12 => Dout12test, Dout13 => Dout13test, Dout14 => Dout14test, Dout15 => Dout15test
        );    
		  
		
clock_process :process  --50% duty cycle
begin
        if (endsim = FALSE) then 
		  clock_test <= '0';
        wait for 5ns;  --for 0.5 ns signal is '0'.
        clock_test <= '1';
        wait for 5ns;  --for next 0.5 ns signal is '1'.
		  else 
				wait;
			end if;
end process clock_process;

--Test Design
test_proc: process(clock_test)
variable clk_counter : integer := 0;
begin 

		if(rising_edge(clock_test)) then
			Din0test <= "00000000";
			Din1test <= "00000001";
			Din2test<=  "00000010";
			Din3test<=  "00000011";
			Din4test<=  "00000100";
			Din5test<=  "00000101";
			Din6test<=  "00000110";
			Din7test<=  "00000111";
			Din8test<=  "00001000";
			Din9test<=  "00001001";
			Din10test<= "00001010";
			Din11test<= "00001011";
			Din12test<= "00001100";
			Din13test<= "00001101";
			Din14test<= "00001110";
			Din15test<= "00001111";

			clk_counter := clk_counter + 1;
			
			if (clk_counter = 1) then
				address_test <= "00";
			elsif (clk_counter = 5) then
				address_test <= "01";
			-- elsif (clk_counter = 10) then
				-- address_test <= "010";
			-- elsif (clk_counter = 15) then
				-- address_test <= "011";
			end if;

		end if;		

  end process test_proc;


  KillClock: process (clock_test)
  variable counter: integer:=0;
  Begin
		if(RISING_EDGE(clock_test)) then
			If(counter <30) then           --after 30 CC kill simulation
				counter := counter + 1;
			else
				endsim := true;
				counter := 0;
			end if;
		else
		
		end if;
  end process;



end architecture test_behaviour;  