# Real-time Asbestos Monitoring System for Sugar Mills

![System Overview](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/system-overview.png)

*The image above shows the system architecture with sensor network, Kafka streaming, processing application, and dashboard.*

## 📋 Overview

The Real-time Asbestos Monitoring System is a comprehensive solution designed specifically for the sugar mill industry to monitor asbestos levels continuously, analyze data in real-time, and provide immediate alerts when safety thresholds are exceeded.

Asbestos exposure remains a significant health concern in many industrial settings, including sugar mills where legacy insulation, gaskets, and other materials may still contain asbestos. This system helps ensure workplace safety through continuous monitoring and early detection of potential hazards.

## 🏭 Industry Application

![Sugar Mill Application](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/sugar-mill-application.png)

*The image shows sensor deployment in typical sugar mill locations - boiler rooms, processing areas, and maintenance sections.*

Sugar mills present unique challenges for asbestos monitoring:
- High temperature environments
- Dusty conditions from sugar processing
- Seasonal operations with maintenance periods
- Legacy equipment and insulation

This system addresses these challenges through:
- Heat-resistant sensors
- Filtering algorithms to distinguish between sugar dust and asbestos fibers
- Comprehensive monitoring during both operational and maintenance periods

## 🔌 System Architecture

![Architecture Diagram](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/architecture-diagram.png)

*The architecture diagram shows data flow from sensors through Kafka to processing and visualization.*

The system consists of four main components:

1. **Sensor Network**: IoT sensors deployed throughout the facility measure airborne asbestos fiber concentrations along with environmental data (temperature, humidity, pressure)

2. **Kafka Messaging System**: Enables real-time data streaming between components with dedicated topics for:
   - Raw sensor readings (`asbestos-sensor-data`)
   - Alert messages (`asbestos-alerts`)
   - Analysis results (`asbestos-analysis`)

3. **Processing Application**: Python-based backend that:
   - Processes incoming sensor data
   - Analyzes readings using statistical and ML methods
   - Generates alerts based on thresholds
   - Performs trend analysis and anomaly detection

4. **Web Dashboard**: Provides visualization and management interface for:
   - Real-time monitoring of all sensors
   - Alert management and history
   - Analysis results and trends
   - System configuration

## ✨ Key Features

![Dashboard Screenshot](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/dashboard-screenshot.png)

*The dashboard screenshot shows the main monitoring interface with real-time readings, alerts panel, and trend graphs.*

- **Real-Time Monitoring**: Continuous collection and visualization of asbestos levels across all monitored locations
- **Multi-threshold Alerts**: Configurable warning and danger thresholds with automated notifications
- **Anomaly Detection**: Machine learning algorithms to identify unusual patterns that may indicate equipment failure or sudden asbestos release
- **Trend Analysis**: Statistical analysis of concentration trends over time with predictive capabilities
- **Historical Data**: Comprehensive storage and querying of historical readings for compliance and analysis
- **RESTful API**: Full featured API for integration with other systems and custom applications
- **Role-based Access**: Different access levels for operators, safety officers, and administrators

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Kafka cluster or Docker-based Kafka setup
- IoT sensors (compatible with the system)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/asbestos-monitoring-system.git
   cd asbestos-monitoring-system
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the Kafka environment:
   ```bash
   docker-compose up -d kafka zookeeper
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:
   ```bash
   python app.py
   ```

6. Access the dashboard at `http://localhost:8000`

### Sensor Configuration

![Sensor Setup](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/sensor-setup.png)

*The image shows the proper installation of a sensor unit with key components labeled.*

Detailed sensor setup instructions can be found in the [Sensor Configuration Guide](docs/sensor-config.md).

## 📊 Dashboard Guide

![Dashboard Annotations](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/dashboard-annotated.png)

*This annotated screenshot explains the different sections and features of the monitoring dashboard.*

The dashboard provides:

1. **Overview Panel**: Summary of all monitored locations with status indicators
2. **Detail View**: Per-location detailed readings and environmental data
3. **Alerts Panel**: Real-time and historical alerts with filtering capabilities
4. **Trend Analysis**: Graphs showing concentration trends over time
5. **System Status**: Health monitoring for all system components

For detailed usage instructions, see the [Dashboard Guide](docs/dashboard-guide.md).

## 🔍 API Documentation

The system provides a comprehensive RESTful API:

- `/sensor-reading/` - POST sensor readings into the system
- `/readings/` - GET sensor readings with filtering options
- `/alerts/` - GET alerts with severity filtering
- `/analysis/` - GET analysis results by location
- `/status/` - GET overall system status

Full API documentation is available at `http://localhost:8000/docs` when the system is running.

## 🛠️ Development

### Project Structure

```
asbestos-monitoring-system/
├── app.py                  # Main application entry point
├── config/                 # Configuration files
├── models/                 # Data models
├── processing/             # Data processing modules
│   ├── anomaly.py          # Anomaly detection algorithms
│   └── thresholds.py       # Threshold checking logic
├── api/                    # API endpoints
├── dashboard/              # Dashboard frontend
├── tests/                  # Test suite
└── docs/                   # Documentation
```

### Running Tests

```bash
pytest
```

### Local Development

For local development without sensors, you can use the simulator:

```bash
python tools/sensor_simulator.py
```

## 📈 Performance Metrics

![Performance Dashboard](https://raw.githubusercontent.com/yourusername/asbestos-monitoring-system/main/docs/images/performance-metrics.png)

*The performance dashboard shows system throughput, latency, and reliability metrics.*

The system is designed to handle:
- Up to 100 sensors reporting at 5-second intervals
- Processing latency under 200ms for alert generation
- 99.9% uptime with failover capabilities
- Data retention configurable from 30 days to 7 years

## 🔒 Safety and Compliance

This system helps sugar mills meet occupational safety requirements by:

- Providing continuous monitoring instead of periodic sampling
- Maintaining comprehensive records for regulatory compliance
- Enabling immediate response to potential exposure situations
- Supporting scheduled reporting for safety audits

**Note**: This system complements but does not replace professional asbestos inspections and testing required by regulations.

## 🤝 Contributing

Contributions are welcome! Please check the [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions, please open an issue on this repository or contact the maintenance team at support@example.com.

---

*Disclaimer: This system is designed to help monitor asbestos levels but should be used as part of a comprehensive asbestos management program that includes professional testing, inspections, and appropriate remediation procedures.*
