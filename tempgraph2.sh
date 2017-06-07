#!/bin/bash
LANG=fi_FI.UTF-8

HOME="/home/pi/code/temperature/"
DIR="/var/www/temperature/"
NOLLA=0

#set to C if using Celsius
#TEMP_SCALE = "C"
 
#define the desired colors for the graphs
INTEMP_COLOR="#CC0000"
OUTTEMP_COLOR="#0000FF"
ZEROTEMP_COLOR="#555555"

#hourly
rrdtool graph $DIR/temp_hourly.png --end now --start -4h \
DEF:temp=$HOME/tempbase2.rrd:temp:AVERAGE \
AREA:temp$INTEMP_COLOR:"Sisällä" \
DEF:outtemp=$HOME/tempbase2.rrd:outtemp:AVERAGE \
LINE1:outtemp$OUTTEMP_COLOR:"Ulkona" \
HRULE:0$ZEROTEMP_COLOR:"Nolla" \
--width 800 --height 600 \
--right-axis 1:0 \
--right-axis-label °C \
--vertical-label °C
 
#daily
rrdtool graph $DIR/temp_daily.png --start -1d \
DEF:temp=$HOME/tempbase2.rrd:temp:AVERAGE \
AREA:temp$INTEMP_COLOR:"Sisällä" \
DEF:outtemp=$HOME/tempbase2.rrd:outtemp:AVERAGE \
LINE1:outtemp$OUTTEMP_COLOR:"Ulkona" \
HRULE:0$ZEROTEMP_COLOR:"Nolla" \
--width 800 --height 600 \
--right-axis 1:0 \
--right-axis-label °C \
--vertical-label °C
 
#weekly
rrdtool graph $DIR/temp_weekly.png --start -1w \
DEF:temp=$HOME/tempbase2.rrd:temp:AVERAGE \
DEF:outtemp=$HOME/tempbase2.rrd:outtemp:AVERAGE \
AREA:temp$INTEMP_COLOR:"Sisällä" \
LINE1:outtemp$OUTTEMP_COLOR:"Ulkona" \
HRULE:0$ZEROTEMP_COLOR:"Nolla" \
--width 800 --height 600 \
--right-axis 1:0 \
--right-axis-label °C \
--vertical-label °C 
 
#monthly
rrdtool graph $DIR/temp_monthly.png --start -1m \
DEF:temp=$HOME/tempbase2.rrd:temp:AVERAGE \
DEF:outtemp=$HOME/tempbase2.rrd:outtemp:AVERAGE \
AREA:temp$INTEMP_COLOR:"Sisällä" \
LINE1:outtemp$OUTTEMP_COLOR:"Ulkona" \
HRULE:0$ZEROTEMP_COLOR:"Nolla" \
--width 800 --height 600 \
--right-axis 1:0 \
--right-axis-label °C \
--vertical-label °C 
 
#yearly
rrdtool graph $DIR/temp_yearly.png --start -1y \
DEF:temp=$HOME/tempbase2.rrd:temp:AVERAGE \
DEF:outtemp=$HOME/tempbase2.rrd:outtemp:AVERAGE \
AREA:temp$INTEMP_COLOR:"Sisällä" \
LINE1:outtemp$OUTTEMP_COLOR:"Ulkona" \
HRULE:0$ZEROTEMP_COLOR:"Nolla" \
--width 800 --height 600 \
--right-axis 1:0 \
--right-axis-label °C \
--vertical-label °C
