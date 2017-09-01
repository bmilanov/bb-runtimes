------------------------------------------------------------------------------
--                                                                          --
--                         GNAT RUN-TIME COMPONENTS                         --
--                                                                          --
--          Copyright (C) 2012-2017, Free Software Foundation, Inc.         --
--                                                                          --
-- GNAT is free software;  you can  redistribute it  and/or modify it under --
-- terms of the  GNU General Public License as published  by the Free Soft- --
-- ware  Foundation;  either version 3,  or (at your option) any later ver- --
-- sion.  GNAT is distributed in the hope that it will be useful, but WITH- --
-- OUT ANY WARRANTY;  without even the  implied warranty of MERCHANTABILITY --
-- or FITNESS FOR A PARTICULAR PURPOSE.                                     --
--                                                                          --
-- As a special exception under Section 7 of GPL version 3, you are granted --
-- additional permissions described in the GCC Runtime Library Exception,   --
-- version 3.1, as published by the Free Software Foundation.               --
--                                                                          --
-- You should have received a copy of the GNU General Public License and    --
-- a copy of the GCC Runtime Library Exception along with this program;     --
-- see the files COPYING3 and COPYING.RUNTIME respectively.  If not, see    --
-- <http://www.gnu.org/licenses/>.                                          --
--                                                                          --
-- GNAT was originally developed  by the GNAT team at  New York University. --
-- Extensive contributions were provided by Ada Core Technologies Inc.      --
--                                                                          --
------------------------------------------------------------------------------

pragma Ada_2012; -- To work around pre-commit check?
pragma Suppress (All_Checks);

--  This initialization procedure mainly initializes the PLLs and
--  all derived clocks.

with Interfaces.STM32;           use Interfaces, Interfaces.STM32;
with Interfaces.STM32.Flash;     use Interfaces.STM32.Flash;
with Interfaces.STM32.PWR;       use Interfaces.STM32.PWR;
with Interfaces.STM32.RCC;       use Interfaces.STM32.RCC;

with System.STM32;               use System.STM32;

procedure Setup_Pll is

   procedure Initialize_Clocks;
   procedure Reset_Clocks;

   ------------------------------
   -- Clock Tree Configuration --
   ------------------------------

   HSE_Enabled  : constant Boolean := False;  -- use high-speed ext. clock
   pragma Unreferenced (HSE_Enabled);

   Activate_PLL : constant Boolean := True;
   pragma Unreferenced (Activate_PLL);

   -----------------------
   -- Initialize_Clocks --
   -----------------------

   --  Clock system is configured as follows:
   --     HSI as input to the PLL
   --     PLL * 10 selected as SYSCLK
   --     (HSI / 2) * 10 = 48MHz
   procedure Initialize_Clocks
   is
   begin
      Flash_Periph.ACR.PRFTBE  := 1;
      Flash_Periph.ACR.LATENCY := 1;

      RCC_Periph.CFGR.HPRE := 0;
      RCC_Periph.CFGR.PPRE := 0;

      RCC_Periph.CFGR.PLLSRC := 0;
      RCC_Periph.CFGR.PLLMUL := 10;
      RCC_Periph.CR.PLLON    := 1;

      loop
         exit when RCC_Periph.CR.PLLRDY = 1;
      end loop;

      RCC_Periph.CFGR.SW := 2;

      loop
         exit when RCC_Periph.CFGR.SWS = 2;
      end loop;
   end Initialize_Clocks;

   ------------------
   -- Reset_Clocks --
   ------------------

   procedure Reset_Clocks is
   begin

      --  Enable HSI
      RCC_Periph.CR.HSION := 1;

      --  Reset SW[1:0], HPRE[3:0], PPRE[2:0] and ADCPRE
      RCC_Periph.CFGR.SW     := 0;
      RCC_Periph.CFGR.HPRE   := 0;
      RCC_Periph.CFGR.PPRE   := 0;
      RCC_Periph.CFGR.ADCPRE := 0;

      --  Reset HSEON, CSSON and PLLON bits
      RCC_Periph.CR.HSEON := 0;
      RCC_Periph.CR.CSSON := 0;
      RCC_Periph.CR.PLLON := 0;

      --  Reset HSEBYP bit
      RCC_Periph.CR.HSEBYP := 0;

      --  Reset PLLSRC, PLLXTPRE, and PLLMUL[3:0] bits
      RCC_Periph.CFGR.PLLSRC   := 0;
      RCC_Periph.CFGR.PLLXTPRE := 0;
      RCC_Periph.CFGR.PLLMUL   := 0;

      --  Reset PREDIV[3:0] bits
      RCC_Periph.CFGR2.PREDIV := 0;

      --  Reset USARTSW[1:0], I2CSW, CECSW and ADCSW bits
      RCC_Periph.CFGR3.USART1SW := 0;
      RCC_Periph.CFGR3.I2C1SW   := 0;
      RCC_Periph.CFGR3.ADCSW    := 0;
      RCC_Periph.CFGR3.USART2SW := 0;

      --  Reset HSI14 bit
      RCC_Periph.CR2.HSI14ON := 0;

      --  Disable all interrupts
      RCC_Periph.CIR := (others => <>);
   end Reset_Clocks;

begin
   Reset_Clocks;
   Initialize_Clocks;
end Setup_Pll;
