#!/bin/bash

# Enhanced Ontology-Driven Stock Analysis System
# Deployment Script

echo "🚀 Enhanced Ontology-Driven Stock Analysis System - Deployment"
echo "================================================================"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  This script should not be run as root for security reasons"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages based on OS
install_package() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y "$1"
        elif command_exists yum; then
            sudo yum install -y "$1"
        elif command_exists dnf; then
            sudo dnf install -y "$1"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command_exists brew; then
            brew install "$1"
        else
            echo "❌ Homebrew not found. Please install Homebrew first."
            exit 1
        fi
    fi
}

# Check Python version
echo "1. Checking Python installation..."
if ! command_exists python3; then
    echo "❌ Python 3 not found. Installing..."
    install_package python3
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "   ✅ Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ Python 3.8+ required. Please upgrade Python."
    exit 1
fi

# Check pip
echo "2. Checking pip installation..."
if ! command_exists pip3; then
    echo "❌ pip3 not found. Installing..."
    install_package python3-pip
fi
echo "   ✅ pip3 found"

# Create virtual environment
echo "3. Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "4. Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"

# Upgrade pip
echo "5. Upgrading pip..."
pip install --upgrade pip
echo "   ✅ pip upgraded"

# Install dependencies
echo "6. Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "   ✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Optional: Install Redis
echo "7. Checking Redis installation..."
if ! command_exists redis-server; then
    echo "   Redis not found. Installing Redis (optional)..."
    install_package redis-server
fi

# Create necessary directories
echo "8. Creating necessary directories..."
mkdir -p cache_dir
mkdir -p models
mkdir -p logs
mkdir -p data
mkdir -p exports
echo "   ✅ Directories created"

# Set permissions
echo "9. Setting permissions..."
chmod +x enhanced_dashboard.py
chmod +x example_usage.py
echo "   ✅ Permissions set"

# Create configuration file
echo "10. Creating configuration..."
cat > config.json << EOF
{
  "debug_mode": false,
  "cache_enabled": true,
  "real_time_enabled": true,
  "ml_enabled": true,
  "max_concurrent_analysis": 10,
  "data_retention_days": 365,
  "ml_model_path": "./models",
  "pattern_recognition_threshold": 0.75,
  "anomaly_detection_threshold": 0.1,
  "max_position_size": 0.10,
  "stop_loss_percentage": 0.05,
  "take_profit_percentage": 0.15,
  "refresh_interval": 30
}
EOF
echo "   ✅ Configuration file created"

# Create systemd service (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "11. Creating systemd service..."
    cat > enhanced-ontology.service << EOF
[Unit]
Description=Enhanced Ontology-Driven Stock Analysis Dashboard
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
ExecStart=$PWD/venv/bin/python enhanced_dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    echo "   ✅ Systemd service file created"
    echo "   📋 To enable service: sudo cp enhanced-ontology.service /etc/systemd/system/"
    echo "   📋 Then run: sudo systemctl enable enhanced-ontology"
fi

# Create startup script
echo "12. Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash

# Enhanced Ontology Dashboard Startup Script

echo "🚀 Starting Enhanced Ontology-Driven Stock Analysis Dashboard..."

# Activate virtual environment
source venv/bin/activate

# Check if Redis is running
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis not running. Starting Redis..."
        redis-server --daemonize yes
        sleep 2
    fi
fi

# Start the dashboard
echo "🌐 Starting web dashboard..."
python enhanced_dashboard.py
EOF

chmod +x start.sh
echo "   ✅ Startup script created"

# Create example runner
echo "13. Creating example runner..."
cat > run_example.sh << 'EOF'
#!/bin/bash

# Run Example Usage Script

echo "🧪 Running example usage..."

# Activate virtual environment
source venv/bin/activate

# Run example
python example_usage.py
EOF

chmod +x run_example.sh
echo "   ✅ Example runner created"

# Create update script
echo "14. Creating update script..."
cat > update.sh << 'EOF'
#!/bin/bash

# Update System Script

echo "🔄 Updating Enhanced Ontology System..."

# Activate virtual environment
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Update dependencies
pip install --upgrade -r requirements.txt

# Save current models
echo "💾 Backing up current models..."
tar -czf models_backup_$(date +%Y%m%d_%H%M%S).tar.gz models/ 2>/dev/null || true

# Update ML models (if available)
echo "🤖 Updating ML models..."
python -c "
from enhanced_ontology_system import enhanced_engine
print('Updating ML models...')
enhanced_engine.save_models()
print('✅ ML models updated')
"

echo "✅ System updated successfully"
EOF

chmod +x update.sh
echo "   ✅ Update script created"

# Final instructions
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "📋 Quick Start Guide:"
echo ""
echo "1. Start the dashboard:"
echo "   ./start.sh"
echo ""
echo "2. Open browser to:"
echo "   http://localhost:8050"
echo ""
echo "3. Run example analysis:"
echo "   ./run_example.sh"
echo ""
echo "4. Update system:"
echo "   ./update.sh"
echo ""
echo "🔧 Configuration:"
echo "   • Edit config.json for custom settings"
echo "   • Modify enhanced_ontology_system.py for custom logic"
echo "   • Update requirements.txt for additional packages"
echo ""
echo "📊 Features Available:"
echo "   • Advanced ontology reasoning"
echo "   • Machine learning integration"
echo "   • Real-time risk management"
echo "   • Pattern recognition"
echo "   • Interactive visualizations"
echo "   • Real-time data streaming"
echo ""
echo "⚠️  Important Notes:"
echo "   • Ensure Redis is running for optimal performance"
echo "   • First analysis may take longer due to model initialization"
echo "   • Monitor system resources for large datasets"
echo "   • Use debug mode for troubleshooting"
echo ""
echo "🆘 Support:"
echo "   • Check README.md for detailed documentation"
echo "   • Review logs in logs/ directory"
echo "   • Enable debug mode in config.json"
echo ""
echo "✨ Happy Trading!"