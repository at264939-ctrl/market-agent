#!/bin/bash

###############################################################################
# Market Intelligence AI Agent - One-Click Runner
# 
# This script sets up and runs the Market Intelligence Agent with colorful
# output and helpful status messages.
#
# Usage: ./run.sh
###############################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Functions
print_header() {
    echo -e "${CYAN}"
    echo -e "╔═══════════════════════════════════════════════════════════╗"
    echo -e "║     📊  Market Intelligence AI Agent                     ║"
    echo -e "║         Automated Company Analysis System                ║"
    echo -e "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}▶${NC} ${BOLD}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${PURPLE}ℹ${NC} $1"
}

check_python() {
    print_step "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Found $PYTHON_VERSION"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version)
        print_success "Found $PYTHON_VERSION"
        return 0
    else
        print_error "Python not found. Please install Python 3.8+"
        return 1
    fi
}

check_env() {
    print_step "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating template..."
        cp .env.example .env 2>/dev/null || echo "Please create .env file manually"
        print_info "Edit .env with your API keys before running"
        return 1
    fi
    
    # Check required variables
    REQUIRED_VARS=("GROQ_API_KEY" "TAVILY_API_KEY" "TWILIO_ACCOUNT_SID" "TWILIO_AUTH_TOKEN")
    MISSING_VARS=()
    
    for var in "${REQUIRED_VARS[@]}"; do
        if ! grep -q "^${var}=" .env 2>/dev/null; then
            MISSING_VARS+=("$var")
        fi
    done
    
    if [ ${#MISSING_VARS[@]} -ne 0 ]; then
        print_warning "Missing environment variables: ${MISSING_VARS[*]}"
        print_info "Please update .env file with your API keys"
        return 1
    fi
    
    print_success "Environment configured"
    return 0
}

install_dependencies() {
    print_step "Installing Python dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        return 1
    fi
    
    # Check if pip is available
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip"
        return 1
    fi
    
    # Install with progress
    $PIP_CMD install -r requirements.txt -q
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed"
        return 0
    else
        print_error "Failed to install dependencies"
        return 1
    fi
}

run_agent() {
    print_step "Starting Market Intelligence Agent..."
    echo ""
    
    # Default companies if not provided
    COMPANIES="${1:-Apple,Microsoft,Google}"
    
    print_info "Analyzing companies: ${CYAN}${COMPANIES}${NC}"
    echo ""
    
    # Run the agent
    python3 main.py --companies "$COMPANIES"
    
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        print_success "Analysis completed successfully!"
        echo ""
        print_info "Reports saved in the current directory"
    else
        print_error "Analysis failed with exit code $EXIT_CODE"
    fi
    
    return $EXIT_CODE
}

show_help() {
    echo -e "${WHITE}"
    echo "Usage: ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -c, --companies     Comma-separated list of companies to analyze"
    echo "  -s, --setup         Only setup (install dependencies)"
    echo "  -n, --no-notif      Disable WhatsApp notifications"
    echo ""
    echo "Examples:"
    echo "  ./run.sh"
    echo "  ./run.sh -c 'Tesla,NVIDIA,AMD'"
    echo "  ./run.sh -c 'Amazon' -n"
    echo "  ./run.sh --setup"
    echo -e "${NC}"
}

# Main script
main() {
    print_header
    
    # Parse arguments
    COMPANIES="Apple,Microsoft,Google"
    SETUP_ONLY=false
    NO_NOTIF=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--companies)
                COMPANIES="$2"
                shift 2
                ;;
            -s|--setup)
                SETUP_ONLY=true
                shift
                ;;
            -n|--no-notif)
                NO_NOTIF=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo ""
    
    # Check Python
    check_python
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    echo ""
    
    # Check environment
    check_env
    ENV_OK=$?
    
    echo ""
    
    # Install dependencies
    install_dependencies
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    echo ""
    
    # If setup only, exit here
    if [ "$SETUP_ONLY" = true ]; then
        print_success "Setup complete!"
        print_info "Now edit .env with your API keys and run ./run.sh again"
        exit 0
    fi
    
    # If environment not configured, show warning
    if [ $ENV_OK -ne 0 ]; then
        echo ""
        print_warning "Skipping analysis - configure .env first"
        print_info "Run './run.sh --setup' to create .env template"
        exit 1
    fi
    
    # Run the agent
    if [ "$NO_NOTIF" = true ]; then
        run_agent "$COMPANIES --no-notification"
    else
        run_agent "$COMPANIES"
    fi
    
    exit $?
}

# Run main function
main "$@"
