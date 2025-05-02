import os
import socket
import subprocess
import platform
import threading
import time
import argparse
import logging
import sys
from ftplib import FTP
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('EthicalSecurityTool')

class EthicalSecurityTool:
    """
    Ethical Security Testing Tool - For educational purposes and authorized testing only
    
    This tool demonstrates common security testing techniques and should ONLY be used:
    - On systems you own
    - On systems you have explicit permission to test
    - In educational environments
    
    IMPORTANT: Unauthorized testing of systems is illegal and unethical.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.disclaimer_accepted = False
        self.current_os = self.detect_os()
        
    def show_disclaimer(self):
        """Display legal disclaimer and require acknowledgment"""
        disclaimer = """
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║                           LEGAL DISCLAIMER                                 ║
        ╠════════════════════════════════════════════════════════════════════════════╣
        ║ This tool is provided for EDUCATIONAL PURPOSES ONLY.                       ║
        ║                                                                            ║
        ║ By proceeding, you agree to:                                               ║
        ║ 1. Only use this tool on systems you OWN or have EXPLICIT PERMISSION       ║
        ║    to test                                                                 ║
        ║ 2. Take full responsibility for any use of this tool                       ║
        ║ 3. Not use this tool for any illegal purposes                              ║
        ║                                                                            ║
        ║ Unauthorized use of this tool against any system is ILLEGAL and may        ║
        ║ result in criminal charges.                                                ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """
        print(disclaimer)
        response = input("\nDo you acknowledge and accept this disclaimer? (yes/no): ").strip().lower()
        if response == 'yes':
            self.disclaimer_accepted = True
            logger.info("Disclaimer accepted. Proceeding with tool initialization.")
            return True
        else:
            logger.warning("Disclaimer not accepted. Exiting tool.")
            return False

    def detect_os(self):
        """Detect the operating system for compatibility purposes"""
        current_os = platform.system()
        if current_os == "Windows":
            return "Windows"
        elif current_os == "Linux":
            return "Linux"
        elif current_os == "Darwin":
            return "MacOS"
        else:
            return "Unknown"

    def ftp_anonymous_login_test(self, target, port=21, timeout=10):
        """
        Test if FTP server allows anonymous login (for educational purposes)
        
        Args:
            target (str): Target IP address or hostname
            port (int): FTP port (default: 21)
            timeout (int): Connection timeout in seconds
        """
        try:
            logger.info(f"Testing FTP anonymous login on {target}:{port} (timeout: {timeout}s)")
            
            # Create FTP connection with timeout
            ftp = FTP(timeout=timeout)
            ftp.connect(target, port)
            
            # Try anonymous login
            ftp.login()
            
            # If we get here, anonymous login succeeded
            logger.info(f"✓ Anonymous FTP login ALLOWED on {target}:{port}")
            logger.info("Directory listing:")
            
            # Get directory listing
            files = []
            ftp.retrlines('LIST', files.append)
            for file in files:
                print(f"  {file}")
            
            # Get welcome message
            print("\nServer welcome message:")
            print(f"  {ftp.getwelcome()}")
            
            # Close connection properly
            ftp.quit()
            logger.info("FTP test completed")
            
            # Security recommendations
            print("\n📋 SECURITY RECOMMENDATIONS:")
            print("  • Disable anonymous FTP access if not required")
            print("  • Implement proper authentication mechanisms")
            print("  • Restrict FTP access to specific IP addresses if possible")
            print("  • Consider using SFTP or FTPS instead of plain FTP")
            
        except Exception as e:
            logger.error(f"FTP anonymous login failed: {e}")
            print("\n📋 RESULTS:")
            print("  • Anonymous FTP login appears to be properly secured")
            print("  • Access denied, as expected in a secure configuration")

    def create_practice_listener(self, listen_ip, port=9999):
        """
        Create a practice listener for educational purposes (similar to netcat)
        
        This is a simplified listener for educational purposes showing how
        a basic command shell works. Only use on authorized systems.
        
        Args:
            listen_ip (str): IP address to listen on
            port (int): Port to listen on
        """
        try:
            # Input validation
            if not self._validate_ip(listen_ip):
                logger.error("Invalid IP address format")
                return
            
            if not self._validate_port(port):
                logger.error("Invalid port number. Use a value between 1024-65535.")
                return
                
            # Create server socket
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind and listen
            logger.info(f"Starting practice listener on {listen_ip}:{port}")
            logger.info("Press Ctrl+C to exit")
            server.bind((listen_ip, port))
            server.listen(1)
            
            # Accept connection
            logger.info("Waiting for incoming connection...")
            client_socket, client_address = server.accept()
            logger.info(f"Connection established from {client_address[0]}:{client_address[1]}")
            
            # Send welcome message
            welcome_msg = "\nWelcome to the Practice Security Tool Shell\n"
            client_socket.send(welcome_msg.encode())
            
            # Interactive shell
            while True:
                # Send prompt
                client_socket.send(b"practice-shell> ")
                
                # Receive command
                command = b""
                while True:
                    char = client_socket.recv(1)
                    if not char or char == b'\n':
                        break
                    command += char
                
                command = command.decode().strip()
                logger.info(f"Received command: {command}")
                
                # Handle exit command
                if command.lower() in ['exit', 'quit', 'bye']:
                    client_socket.send(b"Closing connection. Goodbye!\n")
                    break
                
                # Handle help command
                elif command.lower() == 'help':
                    help_text = """
Available commands:
  help      - Show this help message
  info      - Display system information
  echo      - Echo text back
  time      - Show current time
  exit      - Exit the practice shell

NOTE: This is a LIMITED practice shell for educational purposes.
Real-world security testing requires proper authorization.
"""
                    client_socket.send(help_text.encode())
                
                # Handle info command
                elif command.lower() == 'info':
                    info = f"""
System information:
  Practice Tool Version: {self.version}
  Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  Connection from: {client_address[0]}:{client_address[1]}
"""
                    client_socket.send(info.encode())
                
                # Handle time command
                elif command.lower() == 'time':
                    time_info = f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    client_socket.send(time_info.encode())
                
                # Handle echo command
                elif command.lower().startswith('echo '):
                    echo_text = command[5:] + '\n'
                    client_socket.send(echo_text.encode())
                
                # Handle unknown commands
                else:
                    client_socket.send(b"Unknown command. Type 'help' for available commands.\n")
            
            # Clean up
            client_socket.close()
            server.close()
            logger.info("Listener stopped")
            
        except KeyboardInterrupt:
            logger.info("Practice listener stopped by user")
            try:
                server.close()
            except:
                pass
        except Exception as e:
            logger.error(f"Error in practice listener: {e}")

    def create_practice_client(self, target_ip, port=9999):
        """
        Create a practice client that connects to the listener
        
        Args:
            target_ip (str): Target IP address to connect to
            port (int): Port to connect to
        """
        try:
            # Input validation
            if not self._validate_ip(target_ip):
                logger.error("Invalid IP address format")
                return
            
            if not self._validate_port(port):
                logger.error("Invalid port number. Use a value between 1024-65535.")
                return
                
            # Create client socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            logger.info(f"Connecting to practice listener at {target_ip}:{port}")
            client.connect((target_ip, port))
            logger.info("Connected to practice listener")
            
            # Receive welcome message
            welcome = client.recv(1024).decode()
            print(welcome)
            
            # Interactive shell
            while True:
                # Receive prompt or message
                data = client.recv(1024).decode()
                print(data, end='')
                
                # Get user input
                if data.endswith('> '):
                    user_input = input()
                    client.send((user_input + '\n').encode())
                    
                    # Exit if requested
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        # Wait for response
                        final_msg = client.recv(1024).decode()
                        print(final_msg)
                        break
            
            # Clean up
            client.close()
            logger.info("Connection closed")
            
        except KeyboardInterrupt:
            logger.info("Practice client stopped by user")
            try:
                client.close()
            except:
                pass
        except Exception as e:
            logger.error(f"Error in practice client: {e}")

    def port_scan_demo(self, target, start_port=1, end_port=1024, timeout=1):
        """
        Demonstrate a basic port scanner for educational purposes
        
        Args:
            target (str): Target IP address or hostname
            start_port (int): Starting port number
            end_port (int): Ending port number
            timeout (int): Connection timeout in seconds
        """
        # Input validation
        if not self._validate_ip(target):
            logger.error("Invalid IP address format")
            return
            
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            logger.error("Port range must be between 1-65535")
            return
            
        if end_port < start_port:
            logger.error("End port must be greater than or equal to start port")
            return
            
        if end_port - start_port > 1000:
            response = input("Scanning more than 1000 ports may take a long time. Continue? (yes/no): ").strip().lower()
            if response != 'yes':
                logger.info("Port scan cancelled")
                return
                
        # Common service names
        common_services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP-Alt"
        }
        
        # Start scanning
        open_ports = []
        start_time = time.time()
        logger.info(f"Starting port scan on {target} (ports {start_port}-{end_port})")
        
        for port in range(start_port, end_port + 1):
            try:
                # Create socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)
                
                # Attempt connection
                result = s.connect_ex((target, port))
                if result == 0:
                    service = common_services.get(port, "Unknown")
                    open_ports.append((port, service))
                    logger.info(f"Port {port} ({service}): OPEN")
                s.close()
                
            except KeyboardInterrupt:
                logger.warning("Port scan interrupted by user")
                break
            except:
                pass
        
        # Scan complete
        duration = time.time() - start_time
        logger.info(f"Port scan completed in {duration:.2f} seconds")
        
        # Print results
        if open_ports:
            print("\n📋 SCAN RESULTS:")
            print(f"Target: {target}")
            print(f"Port range: {start_port}-{end_port}")
            print(f"Open ports: {len(open_ports)}")
            print("\nPort  Service")
            print("----- ---------------")
            for port, service in open_ports:
                print(f"{port:<5d} {service}")
                
            # Security recommendations
            print("\n📋 SECURITY RECOMMENDATIONS:")
            print("  • Review open ports and close unnecessary services")
            print("  • Implement firewall rules to restrict access to required services")
            print("  • Ensure all services are updated to the latest versions")
            print("  • Consider using port knocking or VPN for sensitive services")
        else:
            print("\n📋 SCAN RESULTS:")
            print(f"Target: {target}")
            print(f"Port range: {start_port}-{end_port}")
            print("No open ports found in the specified range")

    def dns_lookup_demo(self, target):
        """
        Demonstrate a basic DNS lookup for educational purposes
        
        Args:
            target (str): Target domain name
        """
        try:
            import socket
            
            # Get IP address
            ip_address = socket.gethostbyname(target)
            logger.info(f"DNS lookup for {target}: {ip_address}")
            
            # Get all available information
            try:
                full_info = socket.getaddrinfo(target, None)
                print("\n📋 DNS LOOKUP RESULTS:")
                print(f"Domain: {target}")
                print(f"IP Address: {ip_address}")
                
                # Try to get domain aliases
                try:
                    hostname, aliases, addresses = socket.gethostbyname_ex(target)
                    if aliases:
                        print("\nAliases:")
                        for alias in aliases:
                            print(f"  {alias}")
                    
                    if len(addresses) > 1:
                        print("\nAll IP Addresses:")
                        for addr in addresses:
                            print(f"  {addr}")
                except:
                    pass
                    
            except Exception as e:
                logger.error(f"Error getting additional DNS information: {e}")
                
        except Exception as e:
            logger.error(f"DNS lookup failed: {e}")

    def banner_grabbing_demo(self, target, port):
        """
        Demonstrate banner grabbing for educational purposes
        
        Args:
            target (str): Target IP address or hostname
            port (int): Port to connect to
        """
        try:
            # Input validation
            if not self._validate_port(port):
                logger.error("Invalid port number. Use a value between 1-65535.")
                return
                
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            
            # Connect to server
            logger.info(f"Connecting to {target}:{port} for banner grabbing")
            s.connect((target, port))
            
            # Send HTTP request if it's likely a web server
            if port in [80, 443, 8080, 8443]:
                s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\nUser-Agent: EthicalSecurityTool/1.0\r\n\r\n")
            
            # Receive banner
            banner = s.recv(1024)
            s.close()
            
            # Display banner
            print("\n📋 BANNER GRABBING RESULTS:")
            print(f"Target: {target}:{port}")
            print("\nBanner (raw):")
            print("-" * 50)
            print(banner)
            print("-" * 50)
            
            # Try to decode as text
            try:
                decoded_banner = banner.decode('utf-8', errors='replace')
                print("\nBanner (decoded):")
                print("-" * 50)
                print(decoded_banner)
                print("-" * 50)
            except:
                pass
                
            # Security recommendations
            print("\n📋 SECURITY RECOMMENDATIONS:")
            print("  • Minimize information disclosure in service banners")
            print("  • Remove version information when possible")
            print("  • Use generic banners that don't reveal system details")
            
        except Exception as e:
            logger.error(f"Banner grabbing failed: {e}")

    def whois_lookup_demo(self, target):
        """
        Demonstrate a basic WHOIS lookup for educational purposes
        
        Args:
            target (str): Target domain name
        """
        try:
            # Check if whois module is available
            try:
                import whois
            except ImportError:
                logger.error("The python-whois module is not installed")
                print("To install: pip install python-whois")
                return
                
            # Perform whois lookup
            logger.info(f"Performing WHOIS lookup for {target}")
            result = whois.whois(target)
            
            # Display result
            print("\n📋 WHOIS LOOKUP RESULTS:")
            print(f"Domain: {target}")
            
            # Print key information
            if hasattr(result, "domain_name") and result.domain_name:
                print(f"\nDomain Name: {result.domain_name}")
            
            if hasattr(result, "registrar") and result.registrar:
                print(f"Registrar: {result.registrar}")
                
            if hasattr(result, "creation_date") and result.creation_date:
                if isinstance(result.creation_date, list):
                    print(f"Creation Date: {result.creation_date[0]}")
                else:
                    print(f"Creation Date: {result.creation_date}")
                    
            if hasattr(result, "expiration_date") and result.expiration_date:
                if isinstance(result.expiration_date, list):
                    print(f"Expiration Date: {result.expiration_date[0]}")
                else:
                    print(f"Expiration Date: {result.expiration_date}")
                    
            if hasattr(result, "updated_date") and result.updated_date:
                if isinstance(result.updated_date, list):
                    print(f"Updated Date: {result.updated_date[0]}")
                else:
                    print(f"Updated Date: {result.updated_date}")
                    
            # Print full output
            print("\nFull WHOIS Information:")
            print("-" * 50)
            print(result)
            
        except Exception as e:
            logger.error(f"WHOIS lookup failed: {e}")
            print(f"Error: {e}")

    def _validate_ip(self, ip):
        """Validate IP address format"""
        try:
            socket.inet_aton(ip)
            return True
        except:
            return False
            
    def _validate_port(self, port):
        """Validate port number"""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except:
            return False

    def run(self):
        """Run the main application loop"""
        if not self.show_disclaimer():
            return
            
        self.print_banner()
        self.print_menu()
        
        while True:
            try:
                cmd = input("\nethical-tool> ").strip().lower()
                
                if cmd == "exit":
                    logger.info("Exiting the tool")
                    break
                    
                elif cmd == "help" or cmd == "?":
                    self.print_menu()
                    
                elif cmd == "about":
                    self.print_about()
                    
                elif cmd == "ftp":
                    target = input("Enter target hostname or IP: ")
                    port = input("Enter FTP port [21]: ") or "21"
                    self.ftp_anonymous_login_test(target, int(port))
                    
                elif cmd == "listener":
                    ip = input("Enter IP address to listen on: ")
                    port = input("Enter port to listen on [9999]: ") or "9999"
                    self.create_practice_listener(ip, int(port))
                    
                elif cmd == "client":
                    ip = input("Enter target IP address: ")
                    port = input("Enter target port [9999]: ") or "9999"
                    self.create_practice_client(ip, int(port))
                    
                elif cmd == "scan":
                    target = input("Enter target hostname or IP: ")
                    start = input("Enter starting port [1]: ") or "1"
                    end = input("Enter ending port [1024]: ") or "1024"
                    timeout = input("Enter timeout in seconds [1]: ") or "1"
                    self.port_scan_demo(target, int(start), int(end), float(timeout))
                    
                elif cmd == "dns":
                    target = input("Enter domain name to lookup: ")
                    self.dns_lookup_demo(target)
                    
                elif cmd == "banner":
                    target = input("Enter target hostname or IP: ")
                    port = input("Enter port: ")
                    self.banner_grabbing_demo(target, int(port))
                    
                elif cmd == "whois":
                    target = input("Enter domain name: ")
                    self.whois_lookup_demo(target)
                    
                else:
                    print("Unknown command. Type 'help' for options.")
                    
            except KeyboardInterrupt:
                print("\nInterrupted. Type 'exit' to quit.")
            except Exception as e:
                logger.error(f"Error: {e}")

    def print_banner(self):
        """Print the application banner"""
        banner = f"""
        ╔═══════════════════════════════════════════════════════════════╗
        ║                                                               ║
        ║  ███████╗████████╗██╗  ██╗██╗ ██████╗ █████╗ ██╗              ║
        ║  ██╔════╝╚══██╔══╝██║  ██║██║██╔════╝██╔══██╗██║              ║
        ║  █████╗     ██║   ███████║██║██║     ███████║██║              ║
        ║  ██╔══╝     ██║   ██╔══██║██║██║     ██╔══██║██║              ║
        ║  ███████╗   ██║   ██║  ██║██║╚██████╗██║  ██║███████╗         ║
        ║  ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝         ║
        ║                                                               ║
        ║  ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗║
        ║  ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝║
        ║  ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝ ║
        ║  ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  ║
        ║  ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║   ║
        ║  ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ║
        ║                                                               ║
        ║            Educational Security Testing Tool v{self.version}         ║
        ║                                                               ║
        ║  Operating System: {self.current_os:<39} ║
        ║  Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<40} ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_menu(self):
        """Print the application menu"""
        menu = """
        ╔═══════════════════════════════════════════════════════════════╗
        ║                       AVAILABLE COMMANDS                      ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║  help      - Show this menu                                   ║
        ║  about     - Show information about this tool                 ║
        ║  ftp       - Test for anonymous FTP login                     ║
        ║  listener  - Start a practice network listener                ║
        ║  client    - Connect to a practice listener                   ║
        ║  scan      - Perform a port scan demo                         ║
        ║  dns       - Perform a DNS lookup                             ║
        ║  banner    - Perform banner grabbing                          ║
        ║  whois     - Perform a WHOIS lookup                           ║
        ║  exit      - Exit the tool                                    ║
        ╚═══════════════════════════════════════════════════════════════╝
        """
        print(menu)

    def print_about(self):
        """Print information about the tool"""
        about = f"""
        ╔═══════════════════════════════════════════════════════════════╗
        ║                      ABOUT THIS TOOL                          ║
        ╠═══════════════════════════════════════════════════════════════╣
        ║                                                               ║
        ║  Ethical Security Testing Tool v{self.version}                      ║
        ║                                                               ║
        ║  This tool is designed for educational purposes to help       ║
        ║  understand basic security concepts in a safe and legal       ║
        ║  environment.                                                 ║
        ║                                                               ║
        ║  Features:                                                    ║
        ║  - FTP anonymous login testing                                ║
        ║  - Basic network client/server demonstration                  ║
        ║  - Port scanning demonstration                                ║
        ║  - DNS lookup                                                 ║
        ║  - Banner grabbing                                            ║
        ║  - WHOIS lookup                                               ║
        ║                                                               ║
        ║  REMEMBER: Only use on systems you own or have explicit       ║
        ║  permission to test.                                          ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        
        For ethical hacking resources, consider:
        
        1. Books and courses:
           - "Ethical Hacking and Penetration Testing Guide" by Rafay Baloch
           - "The Web Application Hacker's Handbook" by Dafydd Stuttard
           - SANS SEC560: Network Penetration Testing
        
        2. Practice environments:
           - HackTheBox (hackthebox.com)
           - TryHackMe (tryhackme.com)
           - OWASP WebGoat Project
           - VulnHub (vulnhub.com)
        
        3. Certifications:
           - CompTIA Security+
           - Certified Ethical Hacker (CEH)
           - OSCP (Offensive Security Certified Professional)
        """
        print(about)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Ethical Security Testing Tool')
    parser.add_argument('--version', action='version', version='Ethical Security Testing Tool v1.0.0')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()
    
    # Initialize and run the tool
    tool = EthicalSecurityTool()
    tool.run()


if __name__ == "__main__":
    main()
