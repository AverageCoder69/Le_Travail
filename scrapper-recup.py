import subprocess

try:
    result = subprocess.run(['wget', '--no-check-certificate', '-O', '-', 'https://www.lasecurecrute.fr/recherche'], 
                           capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        html_content = result.stdout
        print(html_content)
    else:
        print(f"Error: {result.stderr}")
        
except subprocess.TimeoutExpired:
    print("Timeout: Request took too long")
except FileNotFoundError:
    print("Error: wget not found. Install with: brew install wget")