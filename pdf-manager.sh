#!/bin/bash

# PDF Manager CLI Helper Script
# This script automatically handles virtual environment activation and runs the PDF Manager CLI

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_MODULE="$SCRIPT_DIR/pdf_manager/cli.py"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_warning "Virtual environment not found. Creating one..."
        python3 -m venv "$VENV_DIR"
        if [ $? -eq 0 ]; then
            print_success "Virtual environment created at $VENV_DIR"
        else
            print_error "Failed to create virtual environment"
            exit 1
        fi
    fi
}

# Function to install dependencies
install_deps() {
    print_info "Checking and installing dependencies..."
    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    pip install --upgrade pip > /dev/null 2>&1

    # Install the package in development mode
    pip install -e "$SCRIPT_DIR" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_warning "Failed to install via pip, falling back to direct execution"
        return 1
    fi

    deactivate
    return 0
}

# Function to run via installed package
run_installed() {
    source "$VENV_DIR/bin/activate"
    pdf-manager "$@"
    local exit_code=$?
    deactivate
    return $exit_code
}

# Function to run directly with Python
run_direct() {
    source "$VENV_DIR/bin/activate"
    python "$PYTHON_MODULE" "$@"
    local exit_code=$?
    deactivate
    return $exit_code
}

# Function to show usage help
show_help() {
    echo "PDF Manager CLI Helper"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "This script automatically manages the virtual environment and runs PDF Manager."
    echo ""
    echo "Commands:"
    echo "  merge      Merge multiple PDF files"
    echo "  walk       Walk through PDF files in a directory"
    echo "  compress   Compress a PDF file"
    echo "  --help     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 merge file1.pdf file2.pdf -o output.pdf"
    echo "  $0 walk ./documents --start 1 --end 10"
    echo "  $0 compress input.pdf output.pdf --compress medium"
    echo ""
    echo "For detailed command help:"
    echo "  $0 merge --help"
    echo "  $0 walk --help"
    echo "  $0 compress --help"
}

# Main execution
main() {
    # Change to script directory
    cd "$SCRIPT_DIR"

    # Handle help requests
    if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        return 0
    fi

    # Special commands
    case "$1" in
        "setup")
            print_info "Setting up PDF Manager..."
            check_venv
            install_deps
            print_success "Setup complete! You can now use: $0 [command]"
            return 0
            ;;
        "status")
            print_info "PDF Manager Status:"
            echo "  Script location: $SCRIPT_DIR"
            echo "  Virtual env: $([ -d "$VENV_DIR" ] && echo "✓ Found" || echo "✗ Missing")"
            echo "  Python module: $([ -f "$PYTHON_MODULE" ] && echo "✓ Found" || echo "✗ Missing")"
            return 0
            ;;
    esac

    # Check if virtual environment exists
    check_venv

    # Try to run via installed package first
    if install_deps; then
        run_installed "$@"
    else
        # Fall back to direct Python execution
        print_info "Running directly with Python..."
        run_direct "$@"
    fi
}

# Run main function with all arguments
main "$@"