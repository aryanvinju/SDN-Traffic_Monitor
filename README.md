# SDN Traffic Monitoring using Ryu and Mininet

## Overview

This project implements a Software Defined Networking (SDN) controller that monitors network traffic and collects flow statistics using the Ryu controller and Mininet emulator.

The controller periodically retrieves flow statistics from switches, including packet count and byte count, and stores them for analysis.

## Features

* Real-time traffic monitoring
* Flow statistics collection
* Packet and byte count tracking
* Periodic polling
* CSV report generation
* Top talker detection

## Technologies Used

* Python
* Ryu SDN Controller
* Mininet
* OpenFlow 1.3
* Docker

## Project Structure

sdn_project/
│── ryu_app/
│   ├── **init**.py
│   └── controller.py
│── traffic_report.csv
│── README.md

## How to Run

### Start the Controller

cd ~/Downloads/sdn_project
sudo docker run --network host -it --rm -v $(pwd):/app -w /app -e PYTHONPATH=/app osrg/ryu ryu-manager ryu_app.controller

### Start Mininet

sudo mn -c
sudo mn --topo single,3 --controller remote --switch ovsk,protocols=OpenFlow13

### Generate Traffic

h1 ping h2

## Output

* Flow statistics displayed in the controller terminal
* CSV file (traffic_report.csv) containing timestamp, flow match, packet count, and byte count

## Working Principle

The controller connects to switches using OpenFlow, periodically requests flow statistics, receives responses, and logs the data while identifying high-traffic flows.

## Applications

* Network monitoring
* Traffic analysis
* SDN learning and experimentation

## Output Screenshots
<img width="975" height="421" alt="image" src="https://github.com/user-attachments/assets/2ba72a42-dfa9-4db4-874b-3664ba2e97bc" />

<img width="975" height="545" alt="image" src="https://github.com/user-attachments/assets/fe652d70-8015-4c34-886b-955547ddad97" />


## Author

Aryan V
