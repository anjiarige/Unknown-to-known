# File: ssl_checker.py

import socket
import ssl
import datetime
from datetime import timezone

def check_ssl_certificate(hostname, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    conn.settimeout(3.0)

    try:
        conn.connect((hostname, port))
        ssl_info = conn.getpeercert()
        expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
        expiry_date = expiry_date.replace(tzinfo=timezone.utc)
        days_left = (expiry_date - datetime.datetime.now(timezone.utc)).days
        print(f"SSL certificate information for {hostname}:")
        print(f"  Valid for: {days_left} days")
        print(f"  Expiry Date: {expiry_date}")
        
        signature_algorithm = ssl_info.get('signatureAlgorithm')
        if signature_algorithm:
            print(f"  Signature Algorithm: {signature_algorithm}")
        else:
            print("  Signature Algorithm: No information available")
    except ssl.SSLCertVerificationError:
        print(f"SSL certificate validation failed for {hostname}!")
    except (socket.timeout, ConnectionRefusedError):
        print(f"Could not establish a connection to {hostname}.")
    except KeyError as e:
        print(f"Error: {str(e)} not found in the SSL certificate.")
    finally:
        conn.close()

if __name__ == "__main__":
    hostname = input("Enter the hostname to check SSL certificate: ")
    check_ssl_certificate(hostname)
