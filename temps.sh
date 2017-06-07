rrdtool create tempbase.rrd \
--start N --step 300  \
DS:in-temp:GAUGE:600:U:U \
DS:out-temp:GAUGE:600:U:U \
RRA:AVERAGE:0.5:1:1440 \
RRA:AVERAGE:0.5:6:10
