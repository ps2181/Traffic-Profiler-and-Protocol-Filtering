
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

### File Structure
ai-network-profiler/
├── README.md                          # Project overview, installation, usage (this file)
├── LICENSE                            # MIT License
├── .gitignore                         # Ignores cache, data, results
├── docker-compose.yml                 # Orchestrates services
├── requirements.txt                   # Core dependencies
├── setup.py                           # Package installation
├── docs/                              # Documentation
│   ├── architecture.md                # System design diagram (text/ASCII art)
│   ├── api-documentation.md           # API specs (OpenAPI/Swagger)
│   ├── deployment-guide.md            # Step-by-step deployment
│   └── research-paper.md              # Novel techniques summary
├── services/                          # Microservices
│   ├── core-profiler/                 # Main analysis engine
│   │   ├── Dockerfile                 # Docker build
│   │   ├── requirements.txt           # Service deps (scapy, torch)
│   │   ├── main.py                    # Entry point (see code below)
│   │   ├── config/                    # Configs
│   │   │   ├── __init__.py
│   │   │   ├── settings.py            # App settings (e.g., anomaly_threshold=0.1)
│   │   │   └── protocol_filters.json  # JSON filters
│   │   ├── models/                    # ML models
│   │   │   ├── __init__.py
│   │   │   ├── anomaly_detector.py    # Autoencoder + Isolation Forest (see code below)
│   │   │   └── llm_query.py           # Novel: LLM integration (placeholder)
│   │   ├── filters/                   # Protocol filters
│   │   │   ├── __init__.py
│   │   │   ├── http_filter.py         # HTTP method filtering (see code below)
│   │   │   ├── dns_filter.py          # DNS query filtering
│   │   │   ├── icmp_filter.py         # ICMP message filtering
│   │   │   └── custom_filter.py       # Extensible filters
│   │   ├── analyzers/                 # Analysis modules
│   │   │   ├── __init__.py
│   │   │   ├── feature_extractor.py   # Packet features (see code below)
│   │   │   ├── anomaly_analyzer.py    # ML anomaly scoring
│   │   │   └── traffic_fingerprint.py # Novel: Device/OS fingerprinting (placeholder)
│   │   └── utils/                     # Utilities
│   │       ├── __init__.py
│   │       ├── cuda_utils.py          # CUDA support (see code below)
│   │       ├── logging_utils.py       # Logging
│   │       └── packet_utils.py        # Scapy helpers
│   │
│   ├── data-service/                  # Data loading and storage
│   │   ├── Dockerfile                 # Docker build
│   │   ├── requirements.txt           # Deps (scapy, pandas)
│   │   ├── main.py                    # Entry point (see code below)
│   │   ├── api/                       # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── data_endpoints.py      # PCAP loading API (see code below)
│   │   ├── loaders/                   # PCAP loaders
│   │   │   ├── __init__.py
│   │   │   ├── pcap_loader.py         # Scapy PCAP reader (see code below)
│   │   │   └── live_loader.py         # Real-time streaming (see code below)
│   │   ├── storage/                   # Storage
│   │   │   ├── __init__.py
│   │   │   ├── file_storage.py        # Local/S3 storage
│   │   │   └── cache_manager.py       # Caching features
│   │   └── preprocessors/             # Preprocessing
│   │       ├── __init__.py
│   │       ├── feature_preprocessor.py # Normalize features
│   │       └── augmentation.py        # Traffic augmentation (placeholder)
│   │
│   ├── visualization-service/         # Visualization and dashboards
│   │   ├── Dockerfile                 # Docker build
│   │   ├── requirements.txt           # Deps (streamlit, plotly)
│   │   ├── main.py                    # Entry point (see code below)
│   │   ├── api/                       # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── viz_endpoints.py       # Plot API (see code below)
│   │   ├── generators/                # Plot generators
│   │   │   ├── __init__.py
│   │   │   ├── plot_generators.py     # Matplotlib/Seaborn (see code below)
│   │   │   ├── interactive_plots.py   # Plotly interactive (placeholder)
│   │   │   └── anomaly_viz.py         # Novel: Anomaly heatmaps (placeholder)
│   │   ├── dashboards/                # Dashboards
│   │   │   ├── __init__.py
│   │   │   ├── streamlit_dashboard.py # Streamlit app (see code below)
│   │   │   └── plotly_dashboard.py    # Plotly Dash (placeholder)
│   │   ├── reports/                   # Reports
│   │   │   ├── __init__.py
│   │   │   ├── pdf_generator.py       # PDF reports (placeholder)
│   │   │   ├── html_reporter.py       # HTML reports (placeholder)
│   │   │   └── summary_generator.py   # Executive summary
│   │   └── templates/                 # Templates
│   │       ├── dashboard.html         # HTML template
│   │       ├── report.html            # Report template
│   │       └── styles.css             # CSS
│   │
│   ├── benchmark-service/             # Performance benchmarking
│   │   ├── Dockerfile                 # Docker build
│   │   ├── requirements.txt           # Deps (thop, onnxruntime)
│   │   ├── main.py                    # Entry point (see code below)
│   │   ├── api/                       # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── benchmark_endpoints.py # Metrics API (see code below)
│   │   ├── profilers/                 # Profilers
│   │   │   ├── __init__.py
│   │   │   ├── latency_profiler.py    # Inference time (see code below)
│   │   │   ├── memory_profiler.py     # Memory usage (placeholder)
│   │   │   └── anomaly_profiler.py    # Anomaly rate profiling
│   │   └── exporters/                 # Exporters
│   │       ├── __init__.py
│   │       ├── json_exporter.py       # JSON output
│   │       └── csv_exporter.py        # CSV for analysis
│   │
│   └── api-gateway/                   # API Gateway
│       ├── Dockerfile                 # Docker build
│       ├── requirements.txt           # Deps (fastapi, uvicorn)
│       ├── main.py                    # Entry point (see code below)
│       ├── middleware/                # Middleware
│       │   ├── __init__.py
│       │   ├── auth.py                # Authentication (placeholder)
│       │   ├── rate_limit.py          # Rate limiting (placeholder)
│       │   └── logging.py             # Request logging (placeholder)
│       ├── routing/                   # Routing
│       │   ├── __init__.py
│       │   └── router.py              # Service routing (see code below)
│       └── config/                    # Config
│           ├── __init__.py
│           └── gateway_config.py      # Gateway settings
│
├── frontend/                          # React.js Frontend
│   ├── package.json                   # Dependencies (React, Tailwind)
│   ├── Dockerfile                     # Docker build
│   ├── public/                        # Public assets
│   │   ├── index.html                 # Entry HTML
│   │   └── manifest.json              # PWA manifest
│   ├── src/                           # Source code
│   │   ├── components/                # Components
│   │   │   ├── Dashboard/             # Main dashboard
│   │   │   │   ├── Dashboard.jsx      # Dashboard (see code below)
│   │   │   │   ├── MetricsPanel.jsx   # Metrics
│   │   │   │   ├── AnomalyViewer.jsx  # Anomaly viz
│   │   │   │   └── RealTimeMonitor.jsx # Real-time streaming
│   │   │   ├── Filters/               # Filter UI
│   │   │   │   ├── ProtocolFilter.jsx # Protocol selector
│   │   │   │   └── AdvancedFilter.jsx # Advanced options
│   │   │   └── Reports/               # Reports
│   │   │       ├── ReportGenerator.jsx # Generate reports
│   │   │       └── ExportPanel.jsx    # Export UI
│   │   ├── services/                  # API services
│   │   │   ├── api.js                 # API calls (see code below)
│   │   │   ├── websocket.js           # Real-time updates (placeholder)
│   │   │   └── auth.js                # Authentication
│   │   ├── utils/                     # Utilities
│   │   │   ├── formatters.js          # Data formatters
│   │   │   └── constants.js           # Protocol constants
│   │   ├── hooks/                     # React hooks
│   │   │   ├── useWebSocket.js        # WebSocket hook
│   │   │   └── useProfiler.js         # Profiler hook
│   │   ├── App.jsx                    # Main app (see code below)
│   │   └── index.js                   # Entry point
│   └── nginx.conf                     # Nginx config
│
├── scripts/                           # Utility Scripts
│   ├── setup/                         # Setup
│   │   ├── install_deps.sh            # Install deps (see code below)
│   │   ├── setup_cuda.sh              # CUDA setup (see code below)
│   │   └── setup_docker.sh            # Docker setup
│   ├── deployment/                    # Deployment
│   │   ├── deploy_local.sh            # Local run (see code below)
│   │   ├── deploy_cloud.sh            # Cloud deployment
│   │   └── update_services.sh         # Service update
│   ├── monitoring/                    # Monitoring
│   │   ├── health_check.py            # Health checks (placeholder)
│   │   ├── resource_monitor.py        # Resource monitoring
│   │   └── alert_manager.py           # Alert handling
│   └── data/                          # Data handling
│       ├── download_pcaps.py          # Download sample PCAPs (see code below)
│       ├── preprocess_pcap.py         # Preprocess PCAP (placeholder)
│       └── validate_pcap.py           # Validate PCAP
│
├── tests/                             # Test Suite
│   ├── unit/                          # Unit tests
│   │   ├── test_filters.py            # Filter tests (see code below)
│   │   ├── test_anomaly_detector.py   # ML tests
│   │   └── test_visualization.py      # Viz tests
│   ├── integration/                   # Integration tests
│   │   ├── test_services.py           # Service integration
│   │   ├── test_pipelines.py          # Pipeline tests
│   │   └── test_streaming.py          # Streaming tests
│   ├── performance/                   # Performance tests
│   │   ├── test_latency.py            # Latency tests
│   │   ├── test_accuracy.py           # Anomaly accuracy
│   │   └── test_scalability.py        # Scalability
│   └── e2e/                           # End-to-End
│       ├── test_full_analysis.py      # Full PCAP analysis
│       └── test_live_stream.py        # Live capture E2E
│
├── configs/                           # Configuration
│   ├── production/                    # Prod configs
│   │   ├── core_profiler.yaml         # Core settings
│   │   ├── data_service.yaml          # Data settings
│   │   └── visualization.yaml         # Viz settings
│   ├── development/                   # Dev configs
│   │   ├── core_profiler.yaml         # Dev core
│   │   ├── data_service.yaml          # Dev data
│   │   └── visualization.yaml         # Dev viz
│   └── protocols/                     # Protocol configs
│       ├── http_config.json           # HTTP filters
│       ├── dns_config.json            # DNS types
│       └── icmp_config.json           # ICMP types
│
├── data/                              # Data (gitignored)
│   ├── pcap_samples/                  # Sample PCAPs
│   ├── models/                        # Trained ML models
│   └── cache/                         # Cached features
│
└── results/                           # Results (gitignored)
    ├── analyses/                      # Analysis outputs
    ├── visualizations/                 # Plot images
    ├── reports/                       # JSON/CSV reports
    └── logs/                          # Logs

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
