

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity LUT is
		port( --address: in STD_LOGIC_VECTOR(14 downto 0);
				--sel_LUT
				address : in STD_LOGIC_VECTOR (1 downto 0); -- 4 cases could be test
				sel_LUT0,sel_LUT1,sel_LUT2,sel_LUT3,sel_LUT4: out STD_LOGIC_VECTOR(2 downto 0)
				
			);
end entity LUT;



architecture selMuxBits of LUT is
begin

-- if (address = 00)
		-- we have default case
-- if address = 01
-- 		we have case for first col
-- if address = 10
--		we have the other case
-- if others , we dont care


		
			MUX0_LUT: process (address) --North out
			begin
				case address is
					when "00" => sel_LUT0  <= "111";
					--when "01" => sel_LUT0  <= "111";
					when "01" => sel_LUT0  <= "111";
					when others => sel_LUT0 <= "111";
				end case;
			end process;
			MUX1_LUT: process (address) --East out
			begin
				case address is
					when "00" => sel_LUT1  <= "111";
					--when "01" => sel_LUT1  <= "100";
					when "01" => sel_LUT1  <= "100";
					when others => sel_LUT1 <= "111";
				end case;
			end process;
			MUX2_LUT: process (address)  --South out
			begin
				case address is
					when "00" => sel_LUT2  <= "111";
					--when "01" => sel_LUT2  <= "011";
					when "01" => sel_LUT2  <= "111";
					when others => sel_LUT2  <= "111";
				end case;
			end process;
			MUX3_LUT: process (address)   --West out
			begin
				case address is
					when "00" => sel_LUT3  <= "111";
					--when "01" => sel_LUT3  <= "111";
					when "01" => sel_LUT3  <= "111";
					when others => sel_LUT3  <= "111";
				end case;
			end process;
			MUX4_LUT: process (address)   --Dout
			begin
				case address is
					when "00" => sel_LUT4  <= "111";
					--when "01" => sel_LUT4  <= "000";
					when "01" => sel_LUT4  <= "011";
					when others => sel_LUT4  <= "111";
				end case;
			end process;

			
end architecture selMuxBits;


