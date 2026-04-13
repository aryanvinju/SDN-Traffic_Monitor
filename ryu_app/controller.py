from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
from ryu.app.simple_switch_13 import SimpleSwitch13
import csv
import time

class TrafficMonitor(SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self.request_stats(dp)
            hub.sleep(5)

    def request_stats(self, datapath):
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        try:
            body = ev.msg.body

            print("\n--- Flow Stats ---")

            # Safe check for empty or None
            if body is None or len(body) == 0:
                print("No flows yet...")
                return

            valid_flows = []

            for stat in body:
                if stat.packet_count > 0:
                    print("Match: {}".format(stat.match))
                    print("Packets: {}".format(stat.packet_count))
                    print("Bytes: {}".format(stat.byte_count))
                    print("Duration: {}s".format(stat.duration_sec))
                    print("-------------------")
                    valid_flows.append(stat)

            # Safe Top Talker
            if len(valid_flows) > 0:
                top_flow = max(valid_flows, key=lambda x: x.byte_count)
                print("Top Talker Bytes: {}".format(top_flow.byte_count))

            self.save_to_csv(valid_flows)

        except Exception as e:
            print("Error in stats handler:", e)

    def save_to_csv(self, stats):
        try:
            with open("traffic_report.csv", "a") as f:
                writer = csv.writer(f)
                for stat in stats:
                    writer.writerow([
                        time.time(),
                        str(stat.match),
                        stat.packet_count,
                        stat.byte_count
                    ])
        except Exception as e:
            print("CSV write error:", e)
