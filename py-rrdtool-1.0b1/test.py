#!/usr/bin/env python
#
# test script for rrd.py
#
#
# Copyright 2006, Red Hat, Inc
# Mihai Ibanescu <misa@redhat.com>
#
# This software may be freely redistributed under the terms of the
# Lesser GNU general public license.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

# Id: test.py 101964 2006-09-08 02:55:53Z misa

import sys
import time
import shutil

import rrdtool as rrd

def main():
    rrd_db = "/tmp/test-rrd"

    shutil.rmtree(rrd_db, ignore_errors=1)

    r = rrd.RoundRobinDatabase(rrd_db)

    heartbeat = 30

    # 30-second PDPs for 8 hours
    r1_steps = 1
    r1_rows = 8 * 3600 / (r1_steps * heartbeat)

    # 5-minute PDPs for 24 hours
    r2_steps = 10
    r2_rows = 24 * 3600 / (r2_steps * heartbeat)

    # 1-hour PDPs for 7 days
    r3_steps = 120
    r3_rows = 7 * 24 * 3600 / (r3_steps * heartbeat)

    # 6-hour PDPs for 30 days
    r4_steps = 6 * 3600 / heartbeat
    r4_rows = 30 * 24 * 3600 / (r4_steps * heartbeat)

    # Attempt to provide enough information for the coarsest grained RRA
    now = int(time.time() / 30) * 30
    first = now - r4_steps * r4_rows * heartbeat

    rras = [ rrd.RoundRobinArchive(cf=rrd.LastCF, xff=0.5, steps=r1_steps,
        rows=r1_rows) ]

    # The steps and rows for each RRA
    srl = [(r2_steps, r2_rows), (r3_steps, r3_rows), (r4_steps, r4_rows)]
    # Consolidation functions
    cfl = [rrd.AverageCF, rrd.MaxCF, rrd.MinCF, rrd.LastCF]

    for steps, rows in srl:
        for cf in cfl:
            rras.append(rrd.RoundRobinArchive(cf=cf, xff=0.5, steps=steps,
                rows=rows))

    r.create(
        rrd.DataSource("tps", type=rrd.GaugeDST, heartbeat=heartbeat),
        rrd.DataSource("rtps", type=rrd.GaugeDST, heartbeat=heartbeat),
        rrd.DataSource("wtps", type=rrd.GaugeDST, heartbeat=heartbeat),
        start=(first-heartbeat), step=heartbeat, *rras)

    template = ('rtps', 'wtps')

    t = first
    while t <= now:
        #r.update(rrd.Val(1, 1, timestamp=t), template=template)
        rps = ((t - first) / heartbeat) % 250
        wps = 250 - ((t - first) / heartbeat) % 250
        tps = max(rps, wps)
        r.update(rrd.Val(tps, rps, wps, timestamp=t))
        t += heartbeat

    g = rrd.RoundRobinGraph("/tmp/test.png")
    g.graph(
        rrd.Def("tps", rrd_db, data_source="tps", cf=rrd.AverageCF),
        rrd.Def("rtps", rrd_db, data_source="rtps", cf=rrd.AverageCF),
        rrd.Def("wtps", rrd_db, data_source="wtps", cf=rrd.AverageCF),
        rrd.LINE1("tps", rrggbb="ff0000", legend="tps"),
        rrd.LINE1("rtps", rrggbb="00ff00", legend="rtps"),
        rrd.LINE1("wtps", rrggbb="0000ff", legend="wtps"),
        alt_y_mrtg=None,
        width=900,
        height=200,
        x="HOUR:1:HOUR:2:HOUR:4:0:%H",
        title="IO stats",
        start=(first - heartbeat),
        end=now,
    )

if __name__ == '__main__':
    sys.exit(main() or 0)
