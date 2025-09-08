import socket
import threading
import time
import errno


def resolve_host(target):
    
    try:
        # Check if already an IP address
        socket.inet_aton(target)
        return target
    except socket.error:
        # Try to resolve hostname
        try:
            ip = socket.gethostbyname(target)
            return ip
        except socket.gaierror:
            print(f"Error: Cannot resolve hostname '{target}'")
            return None


def parse_ports(port_spec):

    ports = []

    # Split by comma for multiple specifications
    parts = port_spec.split(',')

    for part in parts:
        part = part.strip()

        # Check if it's a range
        if '-' in part:
            try:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                
                if start > end or start < 1 or end > 65535:
                    print(f"Invalid port range: {part}")
                    continue

                ports.extend(range(start, end + 1))
            except ValueError:
                print(f"Invalid port range format: {part}")
                continue
        else:
            # Single port
            try:
                port = int(part)
                if 1 <= port <= 65535:
                    ports.append(port)
                else:
                    print(f"Invalid port number: {port}")
            except ValueError:
                print(f"Invalid port: {part}")
                continue

    # Remove duplicates and sort
    ports = sorted(list(set(ports)))
    return ports


def tcp_scan(ip, port, timeout=20):
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            return "open"
        elif result == errno.ECONNREFUSED:
            return "closed"
        else:
            return "filtered"
    except socket.timeout:
        return "filtered"
    except socket.error:
        return "closed"


def scan_port_wrapper(args):
   
    ip, port, timeout = args
    status = tcp_scan(ip, port, timeout)

    # Only skip closed ports
    if status == "closed":
        return None

    try:
        service = socket.getservbyport(port, "tcp")
    except OSError:
        service = "Unknown"

    return (port, status, service)


def display_results(target, ip, ports, results, scan_time):
    print(f"\nTarget: {target} ({ip})")

    # Format port list for display
    if len(ports) <= 10:
        port_list = ','.join(map(str, ports))
    else:
        port_list = f"{ports[0]}-{ports[-1]}"

    print(f"Scanning ports: {port_list}")

    if results:
        print("\nPorts found:")
        # Separate open and filtered ports
        open_ports = [(port, service) for port, status, service in results if status == "open"]
        filtered_ports = [(port, service) for port, status, service in results if status == "filtered"]
        
        # Display open ports
        if open_ports:
            print("\n  Open ports:")
            for port, service in open_ports:
                print(f"    {port}/tcp    open      {service}")
        
        # Display filtered ports
        if filtered_ports:
            print("\n  Filtered ports:")
            for port, service in filtered_ports:
                print(f"    {port}/tcp    filtered  {service}")
    else:
        print("\nNo open or filtered ports found")

    print(f"\nScan completed in {scan_time:.5f} seconds")


def scan_target(target, port_spec):
    
    if not target:
        print("Error: No target specified")
        return

    # Resolve hostname to IP
    ip = resolve_host(target)
    if not ip:
        return

    if not port_spec:
        print("Error: No ports specified")
        return

    # Parse ports
    ports = parse_ports(port_spec)

    if not ports:
        print("Error: No valid ports to scan")
        return

    print(f"\nStarting scan of {len(ports)} ports...")

    # Record start time
    start_time = time.time()

    results = []
    threads = []

    def thread_task(ip, port, timeout):
        result = scan_port_wrapper((ip, port, timeout))
        if result:  # Only add if port is open or filtered
            results.append(result)

    for port in ports:
        t = threading.Thread(target=thread_task, args=(ip, port, 2))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Calculate scan time
    scan_time = time.time() - start_time

    # Sort results by port number
    results.sort()

    # Display results
    display_results(target, ip, ports, results, scan_time)


def main():
   
    print("=" * 60)
    print("                 APEX PORT SCANNER")
    print("=" * 60)
    
    # Example 1: Scan a single port
    print("EXAMPLE 1: Single Port Scan")
    print("-" * 30)
    scan_target("www.speedguide.net", "80")

    print("\n" + "=" * 50 + "\n")

    # Example 2: Scan multiple specific ports
    print("EXAMPLE 2: Multiple Ports Scan")
    print("-" * 30)
    scan_target("scanme.nmap.org", "22,80,443")

    print("\n" + "=" * 50 + "\n")

    # Example 3: Scan a range of ports
    print("EXAMPLE 3: Port Range Scan")
    print("-" * 30)
    scan_target("scanme.nmap.org", "20-25")

    print("\n" + "=" * 50 + "\n")

    # Example 4: Mixed format scan
    print("EXAMPLE 4: Mixed Format Scan")
    print("-" * 30)
    scan_target("www.speedguide.net", "80,443,8080,20-25")


if __name__ == "__main__":
    main()
