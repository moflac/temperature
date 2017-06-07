#define the desired colors for the graphs
INTEMP_COLOR="#CC0000"
OUTTEMP_COLOR="#0000FF"
#hourly
rrdtool graph lampo.png --start -12h \
DEF:mytemp=tempbase.rrd:in-temp:AVERAGE AREA:mytemp#CC0000:"Inside Temperature C" \
DEF:outtemp=tempbase.rrd:out-temp:AVERAGE LINE1:outtemp#00FF00:"Outside Temperature C" \
 --width 800 --height 600
