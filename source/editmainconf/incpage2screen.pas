{ +--------------------------------------------------------------------------+ }
{ | MM8D v0.1 * Growing house controlling and remote monitoring device       | }
{ | Copyright (C) 2020-2021 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incpage2screen.pas                                                       | }
{ | Show screen content of page #2                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page2screen;
var
  b: byte;
begin
  header(PRGNAME+' '+VERSION+' * Page 2/10: Enable/disable channels');
  textcolor(white);
  for b:=1 to 8 do
  begin
    gotoxy(4,b+2);
    write('Channel #'+inttostr(b)+':');
  end;
  for b:=1 to 8 do
  begin
    gotoxy(MINPOSX[2,1],b+2);
    writeln(ena_ch[b]);
  end;
end;
