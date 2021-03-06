#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM8D v0.1 * Growing house controlling and remote monitoring device         |
# | Copyright (C) 2020-2021 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>       |
# | getpage.cgi                                                                |
# | Get data in html format                                                    |
# +----------------------------------------------------------------------------+

#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

# Exit codes:
#   0: normal exit
#   1: cannot open configuration file
#   5: cannot open log file
#   9: no parameter(s)
#  10: bad channel value

use constant USRLOCALDIR => 1;

use lib 'cgi-bin';
use Switch;
use Scalar::Util qw(looks_like_number);

$dark="<font color=\"gray\">&#9679;</font>";
$green="<font color=\"green\">&#9679;</font>";
$red="<font color=\"red\">&#9679;</font>";
$yellow="<font color=\"yellow\">&#9679;</font>";
if (USRLOCALDIR eq 1)
{
  $conffile = "/usr/local/etc/mm8d/mm8d.ini";
  $creatediagprog = "/usr/local/bin/mm8d-creatediagrams";
} else
{
  $conffile = "/etc/mm8d/mm8d.ini";
  $creatediagprog = "/usr/bin/mm8d-creatediagrams";
}

# write header of webpage
sub writeheader()
{
  open HEADER, $headerfile;
  while (<HEADER>)
  {
    chomp;
    print "$_";
  }
  close HEADER;
}

# write footer of webpage
sub writefooter()
{
  open FOOTER, $footerfile;
  while (<FOOTER>)
  {
    chomp;
    print "$_";
  }
  close FOOTER;
}

# write table on webpage
sub writetable()
{
  my(@columns)= split(",");
  my($colnum)=$#columns;
  $row = "";
  foreach $colnum (@columns)
  {
    $row = $row . $colnum;
  }
  my(@datarow) = split("\"\"",$row);
  my($datarownum) = $#datarow;
  print "        <tr align=\"center\">";
  $shortdate = substr($columns[0],5,5);
  print "          <td>$shortdate</td>";
  print "          <td>$columns[1]</td>";
  if ($channel == 0)
  {
    if ($columns[2] eq 1) { $columns[2] = $red } else { $columns[2] = $dark };
    if ($columns[3] eq 1) { $columns[3] = $red } else { $columns[3] = $dark };
    if ($columns[4] eq 1) { $columns[4] = $red } else { $columns[4] = $dark };
    if ($columns[5] eq 1) { $columns[5] = $red } else { $columns[5] = $dark };
    print "          <td>$columns[2]</td>";
    print "          <td>$columns[3]</td>";
    print "          <td>$columns[4]</td>";
    print "          <td>$columns[5]</td>";
  } else
  {
    print "          <td>$columns[2]</td>";
    print "          <td>$columns[3]</td>";
    print "          <td>$columns[4]</td>";
    if ($columns[5] eq 1) { $columns[5] = "H" } else { $columns[5] = "M" };
    if ($columns[6] eq 1) { $columns[6] = $yellow } else { $columns[6] = $dark };
    if ($columns[7] eq 1) { $columns[7] = $red } else { $columns[7] = $dark };
    if ($columns[8] eq 1) { $columns[8] = $red } else { $columns[8] = $dark };
    if ($columns[9] eq 1) { $columns[9] = $green } else { $columns[9] = $dark };
    if ($columns[10] eq 1) { $columns[10] = $green } else { $columns[10] = $dark };
    if ($columns[11] eq 1) { $columns[11] = $green } else { $columns[11] = $dark };
    print "          <td>$columns[5]</td>";
    print "          <td>$columns[6]</td>";
    print "          <td>$columns[7]</td>";
    print "          <td>$columns[8]</td>";
    print "          <td>$columns[9]</td>";
    print "          <td>$columns[10]</td>";
    print "          <td>$columns[11]</td>";
  }
  print "        </tr>";
}

# get data
local ($buffer, @pairs, $pair, $name, $value, %FORM);
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "GET")
{
  $buffer = $ENV{'QUERY_STRING'};
}

# split input data
@pairs = split(/&/, $buffer);
foreach $pair (@pairs)
{
  ($name, $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%(..)/pack("C", hex(1))/eg;
  $FORM{$name} = $value;
}
$channel = $FORM{channel};
if ($channel eq '')
{
  print "Content-type:text/plain\r\n\r\n";
  print "ERROR #9\n";
  print "Usage: getpage.cgi?channel=...\n";
  exit 9;
}

# load configuration
if (-e $conffile)
{
  open CONF, "< $conffile";
  while (<CONF>)
  {
    chop;
    my(@columns) = split("=");
    my($colnum) = $#columns;
    $row = "";
    foreach $colnum (@columns)
    {
      $row = $row . $colnum;
    }
    my(@datarow) = split("\"\"",$row);
    my($datarownum) = $#datarow;
    switch ($columns[0])
    {
      case "cam_show" { $cam_show = $columns[1]; }
      case "dir_htm" { $dir_htm = $columns[1]; }
      case "dir_lck" { $dir_lck = $columns[1]; }
      case "dir_log" { $dir_log = $columns[1]; }
      case "dir_msg" { $dir_msg = $columns[1]; }
      case "dir_shr" { $dir_shr = $columns[1]; }
      case "lng" { $lang = $columns[1]; }
      case "usr_dt1" { $usr_dt1 = $columns[1]; }
      case "web_lines" { $web_lines = $columns[1]; }
    }
    my @b = (0..8);
    for (@b)
    {
      if ($columns[0] eq "nam_ch" . $_)
      {
        $nam_ch[$_] = $columns[1];
      }
    }
  }
  close CONF;
} else
{
  print "Content-type:text/plain\r\n\r\n";
  print "ERROR #1:\n";
  print "Cannot open ",$conffile," configuration file!\n";
  exit 1;
}

# load messages
$msg01 = "MM8D";
$msg08 = "Channel";
$msg10 = "Names";
$msg11 = "Temperature in &deg;C";
$msg12 = "Relative humidity in %";
$msg13 = "Relative gas concentrate in %";
$msg17 = "Operation mode (hyphae/mushroom)";
$msg18 = "Manual operation";
$msg19 = "Overcurrent breakers";
$msg20 = "Alarm";
$msg21 = "Lamp output";
$msg22 = "Ventilator output";
$msg23 = "Heater output";
$msg24 = "Date";
$msg25 = "Time";
$msg26 = "Latest status";
$msg27 = "Refresh";
$msg28 = "Camera";
$msg29 = "Log";
$msg30 = "Login via SSH and run <i>mm8d-viewlog</i> to see full log.";
$msg31 = "Start page";
$msg32 = "Mains voltage sensor";
$msg33 = "Overcurrent breaker";

$msgfile = "$dir_msg/$lang/mm8d.msg";
open MSG, "< $msgfile";
while(<MSG>)
{
  chop;
  my(@columns) = split("=");
  my($colnum) = $#columns;
  $row = "";
  foreach $colnum (@columns)  
  {
    $row = $row . $colnum;
  }
  my(@datarow) = split("\"\"",$row);
  my($datarownum) = $#datarow;
  switch ($columns[0])
  {
    case "msg01" { $msg01 = $columns[1]; }
    case "msg08" { $msg08 = $columns[1]; }
    case "msg10" { $msg10 = $columns[1]; }
    case "msg11" { $msg11 = $columns[1]; }
    case "msg12" { $msg12 = $columns[1]; }
    case "msg13" { $msg13 = $columns[1]; }
    case "msg17" { $msg17 = $columns[1]; }
    case "msg18" { $msg18 = $columns[1]; }
    case "msg19" { $msg19 = $columns[1]; }
    case "msg20" { $msg20 = $columns[1]; }
    case "msg21" { $msg21 = $columns[1]; }
    case "msg22" { $msg22 = $columns[1]; }
    case "msg23" { $msg23 = $columns[1]; }
    case "msg24" { $msg24 = $columns[1]; }
    case "msg25" { $msg25 = $columns[1]; }
    case "msg26" { $msg26 = $columns[1]; }
    case "msg27" { $msg27 = $columns[1]; }
    case "msg28" { $msg28 = $columns[1]; }
    case "msg29" { $msg29 = $columns[1]; }
    case "msg30" { $msg30 = $columns[1]; }
    case "msg31" { $msg31 = $columns[1]; }
    case "msg32" { $msg32 = $columns[1]; }
    case "msg33" { $msg33 = $columns[1]; }
  }
}
close MSG;

# set filenames
$footerfile = "$dir_shr/footer_$lang.html";
$headerfile = "$dir_shr/header_$lang.html";
$lockfile = "$dir_lck/mm8d.lock";
$logfile = "$dir_log/mm8d-ch";
if ( looks_like_number($channel) && $channel >=0  &&  $channel <= 8 )
{
  $ch = $channel;
} else
{
  print "Content-type:text/plain\r\n\r\n";
  print "ERROR #10\n";
  print "Bad channel value!\n";
  exit 10;
}
$logfile = $logfile . $ch . ".log";

# create diagram pictures
if ($channel > 0) { system("$creatediagprog $channel"); }

# create output
print "Content-type:text/html\r\n\r\n";
writeheader();
while (-e $lockfile)
{
  sleep 1;
}
print "    <table border=\"0\" cellspacing=\"0\" cellpadding=\"6\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <td colspan=\"2\" class=\"header\" align=\"center\">";
print "            <b class=\"title0\">$msg08 #$ch</b>";
print "          </td>";
print "        </tr>";
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <b class=\"title1\">$msg10</b><br>";
print "    <br>";
print "    <table border=\"0\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
if ($channel == 0)
{
  print "        <tr><td align=\"right\"><b>1:</b></td><td>$msg32</td></tr>";
  print "        <tr><td align=\"right\"><b>2:</b></td><td>$msg33 #1</td></tr>";
  print "        <tr><td align=\"right\"><b>3:</b></td><td>$msg33 #2</td></tr>";
  print "        <tr><td align=\"right\"><b>4:</b></td><td>$msg33 #3</td></tr>";
} else
{
  print "        <tr><td align=\"right\"><b>1:</b></td><td>$msg11</td></tr>";
  print "        <tr><td align=\"right\"><b>2:</b></td><td>$msg12</td></tr>";
  print "        <tr><td align=\"right\"><b>3:</b></td><td>$msg13</td></tr>";
  print "        <tr><td align=\"right\"><b>4:</b></td><td>$msg17</td></tr>";
  print "        <tr><td align=\"right\"><b>5:</b></td><td>$msg18</td></tr>";
  print "        <tr><td align=\"right\"><b>6:</b></td><td>$msg19</td></tr>";
  print "        <tr><td align=\"right\"><b>7:</b></td><td>$msg20</td></tr>";
  print "        <tr><td align=\"right\"><b>8:</b></td><td>$msg21</td></tr>";
  print "        <tr><td align=\"right\"><b>9:</b></td><td>$msg22</td></tr>";
  print "        <tr><td align=\"right\"><b>10:</b></td><td>$msg23</td></tr>";
}
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <b class=\"title1\">$msg26</b><br>";
print "    <br>";
print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <th>$msg24</th><th>$msg25</th>";
if ($channel == 0)
{
  print "          <th>1</th><th>2</th><th>3</th><th>4</th>";
} else
{
  print "          <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>";
  print "          <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>";
}
print "        </tr>";
if (-e $logfile)
{
  open DATA, "< $logfile";
  while (<DATA>)
  {
    chop;
    writetable();
    last;
  }
  close DATA;
} else
{
  print "      </tbody>";
  print "    </table>";
  print "    <br>";
  print "    ERROR #5: Cannot open ",$logfile," log file!";
  print "    <br>";
  print "    <br>";
  print "    <center>";
  print "      <a href=/index.html><input value=\"$msg31\" type=\"submit\"></a>";
  print "    </center>";
  print "    <br>";
  writefooter();
  exit 5;
}
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <center>";
print "      <a href=/index.html><input value=\"$msg31\" type=\"submit\"></a>";
print "      <a href=/cgi-bin/getpage.cgi?channel=$channel><input value=\"$msg27\" type=\"submit\"></a>";
print "    </center>";
print "    <br>";
print "    <hr>";
print "    <br>";
if (($cam_show eq 1) and ($channel > 0))
{
  print "    <b class=\"title1\">$msg28</b><br>";
  print "    <br>";
  print "    <br>";
  print "    <table border=\"1\" cellpadding=\"20\" cellspacing=\"0\" width=\"100%\">";
  print "      <tbody>";
  print "        <tr>";
  print "          <td width=\"50%\"><img src=\"/snapshots/camera-ch$ch.jpg\" width=\"100%\"></td>";
  print "        </tr>";
  print "      </tbody>";
  print "    </table>";
  print "    <br>";
  print "    <hr>";
  print "    <br>";
}
print "    <b class=\"title1\">$msg29</b><br>";
print "    <br>";
print "    <br>";
if ($channel > 0)
{
  print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
  print "      <tbody>";
  print "        <tr><td><img src=\"/diagrams/temperature-ch$ch.png\" width=\"100%\"></td></tr>";
  print "        <tr><td><img src=\"/diagrams/humidity-ch$ch.png\" width=\"100%\"></td></tr>";
  print "        <tr><td><img src=\"/diagrams/gasconcentrate-ch$ch.png\" width=\"100%\"></td></tr>";
  print "      </tbody>";
  print "    </table>";
  print "    <br>";
}
print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <th>$msg24</th><th>$msg25</th>";
if ($channel == 0)
{
  print "          <th>1</th><th>2</th><th>3</th><th>4</th>";
} else
{
  print "          <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>";
  print "          <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>";
}
print "        </tr>";
$line = 0;
if (-e $logfile)
{
  open DATA, "< $logfile";
  while (<DATA>)
  {
    chop;
    writetable();
    $line = $line + 1;
    if ($line eq $web_lines) { last };
  }
  close DATA;
} else
{
  print "      </tbody>";
  print "    </table>";
  print "    <br>";
  print "ERROR #5: Cannot open ",$logfile," log file!";
  print "    <br>";
  writefooter();
  exit 5;
}
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    $msg30";
print "    <br>";
writefooter();
exit 0;
