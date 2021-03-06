{ +--------------------------------------------------------------------------+ }
{ | MM8D v0.1 * Growing house controlling and remote monitoring device       | }
{ | Copyright (C) 2020-2021 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incpage1screen.pas                                                       | }
{ | Show screen content of page #1                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page1screen;
var
  b: byte;
begin
  header(PRGNAME+' '+VERSION+' * Override output status');
  textcolor(white);
  gotoxy(4,3); writeln('Output #1 - lamp:');
  gotoxy(4,4); writeln('Output #2 - ventilator:');
  gotoxy(4,5); writeln('Output #3 - heater:');
  for b:=1 to 3 do
  begin
    gotoxy(30,2+b); writeln(outputs[b]);
  end;
end;
