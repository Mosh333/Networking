
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std;

entity test_bench_2a is

end entity;

architecture test_behaviour of test_bench_2a is 

Shared variable endsim : boolean := FALSE;
Shared variable W : integer := 8;

--components
component lab2a is --instantiate a lab2a component
-- Component Declaration for the Unit Under Test (UUT)


generic (W: integer := 8);
port(	in0, in1, in2, in3, in4: in STD_LOGIC_VECTOR(W-1 downto 0);
out0r, out1r, out2r, out3r, out4r : out STD_LOGIC_VECTOR(W-1 downto 0);
clock, clear :			 in  std_logic;
adrPort: in STD_LOGIC_VECTOR(1 downto 0));

end component;

------------------------
--define signals below




signal in0_test, in1_test, in2_test, in3_test, in4_test: STD_LOGIC_VECTOR(W-1 downto 0);  --unsigned
signal out0r_test, out1r_test, out2r_test, out3r_test, out4r_test: STD_LOGIC_VECTOR(W-1 downto 0);
signal clock_test : STD_LOGIC;
signal clear_test: STD_LOGIC;
signal address_test: STD_LOGIC_VECTOR(1 downto 0);


begin


 -- Instantiate the Unit Under Test (UUT)
   uut: lab2a generic map(w) PORT MAP (            --double check which signals are to be kept
			clock=>clock_test, clear => clear_test,
			in0=>in0_test, in1=>in1_test, in2=>in2_test, in3=>in3_test, in4=>in4_test,
			out0r=>out0r_test, out1r=>out1r_test, out2r=>out2r_test, out3r=>out3r_test, out4r=>out4r_test,
			adrPort => address_test
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
			in0_test <= "00000000";
			in1_test <= "00000001";
			in2_test <= "00000010";
			in3_test <= "00000011";
			in4_test <= "00000100";
			clk_counter := clk_counter + 1;
			
			if (clk_counter = 1) then
				address_test <= "00";
			elsif (clk_counter = 5) then
				address_test <= "01";
			elsif (clk_counter = 10) then
				address_test <= "10";
			elsif (clk_counter = 15) then
				address_test <= "11";
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