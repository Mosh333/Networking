

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity LUT is
		port( --address: in STD_LOGIC_VECTOR(14 downto 0);
				--sel_LUT
				sel_LUT0,sel_LUT1,sel_LUT2,sel_LUT3,sel_LUT4: out STD_LOGIC_VECTOR(2 downto 0);
				address : in STD_LOGIC_VECTOR (1 downto 0) -- 4 cases could be test
				
		);
end entity LUT;


architecture selMuxBits of LUT is
begin
process (address) begin
		case address is 
			when "00" =>
				sel_LUT0  <= "000";
				sel_LUT1  <= "001";
				sel_LUT2  <= "010";
				sel_LUT3  <= "011";
				sel_LUT4  <= "100";
			when "01" =>
				sel_LUT0  <= "001";
				sel_LUT1  <= "010";
				sel_LUT2  <= "011";
				sel_LUT3  <= "100";
				sel_LUT4  <= "000";
			when "10" =>
				sel_LUT0  <= "010";
				sel_LUT1  <= "011";
				sel_LUT2  <= "100";
				sel_LUT3  <= "000";
				sel_LUT4  <= "001";
			when "11" =>
				sel_LUT0  <= "011";
				sel_LUT1  <= "100";
				sel_LUT2  <= "000";
				sel_LUT3  <= "001";
				sel_LUT4  <= "010";
			when 
				others => null;
		end case;
end process;

end architecture selMuxBits;