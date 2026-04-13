SDN Traffic Monitoring Project

SETUP:

1. Install dependencies:
   pip install ryu

2. Run controller:
   ryu-manager controller.py

3. Run Mininet:
   sudo mn --topo single,3 --controller remote --switch ovsk,protocols=OpenFlow13

4. Generate traffic:
   h1 ping h2
   OR
   iperf h1 h2

OUTPUT:
- Flow stats printed in terminal
- CSV file generated: traffic_report.csv
