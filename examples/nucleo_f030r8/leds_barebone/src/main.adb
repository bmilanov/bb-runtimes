--  Program that flashes LD2 (PA05) on the board each second.

pragma Warnings(Off);
with Interfaces.STM32; use Interfaces.STM32;
pragma Warnings(On);

with Ada.Real_Time;

with System;

procedure Main is

   package RT renames Ada.Real_Time;

   RCC_AHBENR    : UInt32;
   GPIOA_MODER   : UInt32;
   GPIOA_OSPEEDR : UInt32;
   GPIOA_PUPDR   : UInt32;
   GPIOA_ODR     : UInt32;

   Period        : constant RT.Time_Span := RT.Milliseconds (500);

   for RCC_AHBENR'Address    use System'To_Address (16#4002_1014#);
   for GPIOA_MODER'Address   use System'To_Address (16#4800_0000#);
   for GPIOA_OSPEEDR'Address use System'To_Address (16#4800_0008#);
   for GPIOA_PUPDR'Address   use System'To_Address (16#4800_000C#);
   for GPIOA_ODR'Address     use System'To_Address (16#4800_0014#);

begin
   --  Initialization is as follows:
   --     Enable GPIOA in RCC
   --     Configure LD2 (PA05) as General purpose output mode
   --     Configure LD2 (PA05) as High speed
   --     Configure LD2 (PA05) as Pull-up
   RCC_AHBENR    := RCC_AHBENR    or 16#2_0000#;
   GPIOA_MODER   := GPIOA_MODER   or 16#400#;
   GPIOA_OSPEEDR := GPIOA_OSPEEDR or 16#C00#;
   GPIOA_PUPDR   := GPIOA_PUPDR   or 16#400#;

   loop
      declare
         use RT;
      begin
         --  Turn LD2 (PA05) on
         GPIOA_ODR := GPIOA_ODR or 16#20#;
         delay until Clock + Period;

         --  Turn LD2 (PA05) off
         GPIOA_ODR := GPIOA_ODR and 16#FFFF_FFDF#;
         delay until Clock + Period;
      end;
   end loop;
end Main;
