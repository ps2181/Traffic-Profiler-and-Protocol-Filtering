
# Advanced AI-Enhanced Network Traffic Profiler

## Overview

The **Advanced AI-Enhanced Network Traffic Profiler** is an open-source tool for analyzing PCAP files and live network traffic with AI-driven anomaly detection and protocol filtering. Built with Scapy, PyTorch, and FastAPI, it supports real-time streaming, ML-based anomaly scoring (autoencoder + Isolation Forest), and interactive visualizations. This project focuses on cybersecurity applications, such as malware detection in email attachments and intrusion analysis. Developed by Pritam Satpathy, it is OSS-ready and extensible for community contributions as of October 16, 2025.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Protocols](#supported-protocols)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Visualizations](#visualizations)
- [Extensibility and Future Features](#extensibility-and-future-features)
- [License](#license)
- [Contact](#contact)
- [Changelog](#changelog)

## Features

### Core Features
- **Protocol Filtering**: Filter by HTTP methods, DNS query types, ICMP message types.
- **AI Anomaly Detection**: Unsupervised ML using autoencoder for reconstruction error + Isolation Forest for outlier detection.
- **Real-Time Streaming**: Asyncio-based live capture with on-the-fly anomaly alerts.
- **Feature Extraction**: Numerical vectors from packets (size, timing, entropy) for AI input.
- **Microservices**: Core profiler, data service, visualization service for scalability.
- **Benchmarking**: Measures anomaly rate, session duration, packet distribution.

### Additional Features
- **Advanced Visualizations**: 2x2 dashboards (packet size, protocol pie, anomaly timeline, session histograms).
- **LLM Integration**: Optional LLM for natural language query on traffic logs (e.g., "find suspicious DNS").
- **CUDA Support**: GPU acceleration for anomaly detection.

## Installation

### Prerequisites
- **OS**: Linux/macOS (Windows via WSL).
- **Python**: 3.8+.
- **Dependencies**: Scapy, PyTorch (CUDA optional), FastAPI, Matplotlib, Scikit-learn.
- **Tools**: Docker for microservices.

### Steps
1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-network-profiler.git
   cd ai-network-profiler
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup CUDA (Optional)**:
   ```bash
   ./scripts/setup_cuda.sh
   ```

4. **Build and Run**:
   ```bash
   docker-compose up --build
   ```

5. **Verify**:
   - Access dashboard: `http://localhost:3000`.
   - Run profiler: `python main.py -p sample.pcap -i 192.168.1.1`.

## Usage

### Offline PCAP Analysis
```bash
python main.py -p capture.pcap -i 192.168.1.1 -m GET POST -q 1 12 -t 8 -o profile.json
```
- Filters HTTP (GET/POST), DNS (types 1,12), ICMP (type 8).
- Outputs JSON with profile and anomalies; generates `traffic_visualization.png`.

### Live Streaming
```bash
python main.py -s eth0 -d 60 -i 192.168.1.1
```
- Captures on interface `eth0` for 60s, alerts on anomalies >10%.

### API Usage
- Start services: `docker-compose up`.
- Query core profiler: `curl http://localhost:5000/analyze -d '{"pcap": "capture.pcap", "ip": "192.168.1.1"}'`.

## Supported Protocols

- **HTTP**: Filter by methods (GET, POST, etc.); entropy analysis for evasion.
- **DNS**: Query types (A=1, PTR=12); anomaly on unusual queries.
- **ICMP**: Message types (Echo Request=8); detect scans.
- **Extensible**: Add filters in `app_filters` dict (e.g., 'SSH': 'tcp port 22').

## Architecture

### High-Level Design
- **core-profiler**: Analyzes PCAP, runs ML anomaly detection.
- **data-service**: Loads PCAP files, extracts features.
- **visualization-service**: Generates plots and dashboards.
- **benchmark-service**: Profiles performance (latency, throughput).
- **api-gateway**: Routes requests.

### Data Flow
PCAP → Data-Service (load/extract) → Core-Profiler (filter/anomaly) → Benchmark-Service (metrics) → Visualization-Service (plots).

### Technology Stack
- **Backend**: Python, Scapy, PyTorch (for autoencoder), FastAPI.
- **AI/ML**: Autoencoder + Isolation Forest for anomalies.
- **Frontend**: React with Tailwind for dashboard.
- **Containerization**: Docker, Docker Compose.
- **Monitoring**: Optional Prometheus/Grafana.

## Contributing

### Guidelines
1. Fork the repo and create a feature branch (`git checkout -b feature/anomaly-v2`).
2. Install deps and run tests (`pytest tests/`).
3. Commit changes (`git commit -m "Add LLM integration"`).
4. Push and open a PR.

### Development Setup
- Run `scripts/setup_dev.sh` for local env.
- Tests: `pytest -v tests/`.
- Lint: `flake8 .`.

### Community
- Issues: Report bugs or request features.
- Discussions: Share ideas for extensions.

## Visualizations

### Generated Outputs
- **Packet Size Distribution**: Histogram of IP lengths.
- **Protocol Breakdown**: Pie chart of protocols.
- **Anomaly Timeline**: Scatter plot highlighting anomalies.
- **Session Duration**: Histogram of session times.

### Access
- Run visualization-service: View at `http://localhost:3000`.
- Export: PNG/PDF via API.

## Extensibility and Future Features

### Current Extensibility
- **Add Protocols**: Extend `app_filters` and filter functions.
- **New ML Models**: Swap autoencoder in `TrafficAnomalyDetector` with LSTM for sequences.
- **Datasets**: Add live feeds from Wireshark or Zeek logs.

### Future Features
- **LLM Integration**: Use LLMs (e.g., GPT-4) for natural language queries (e.g., "find suspicious DNS").
- **Real-Time Alerts**: WebSocket notifications for anomalies.
- **Federated Learning**: Distributed anomaly detection across networks.
- **Quantum-Inspired Detection**: Use quantum algorithms for pattern matching (research phase).
- **Edge Deployment**: TFLite export for mobile/embedded devices.
- **Multi-Modal Analysis**: Combine with endpoint logs for holistic profiling.

### Roadmap
- **v1.1 (Q1 2026)**: LLM queries and WebSocket alerts.
- **v1.2 (Q2 2026)**: Federated learning support.
- **v2.0 (Q3 2026)**: Quantum-inspired features.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contact

- **Author**: Pritam Satpathy
- **Email**: hellopritam31@gmail.com
- **GitHub**: [github.com/pritam31](https://github.com/pritam31)
- **Issues**: [GitHub Issues](https://github.com/pritam31/ai-network-profiler/issues)

## Changelog

### October 16, 2025
- Initial release with ML anomaly detection and real-time streaming.
- Added protocol filtering and visualizations.

### Future
- LLM integration for semantic analysis (Q1 2026).
- Federated learning for distributed networks (Q2 2026).
```
