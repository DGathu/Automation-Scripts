import os
import sys

def create_virtual_environment(venv_name):
    try:
        # Create the virtual environment
        os.system(f'python -m venv {venv_name}')
        print(f"Virtual environment '{venv_name}' created successfully.")
        
        # Activate the virtual environment
        if sys.platform == "win32":
            activate_script = f"{venv_name}\\Scripts\\activate"
        else:
            activate_script = f"{venv_name}/bin/activate"
        
        print(f"To activate the virtual environment, run:")
        print(f"source {activate_script}")
    
    except Exception as e:
        print(f"An error occurred while creating the virtual environment: {e}")

def main():
    venv_name = input("Enter the name for the virtual environment: ")
    create_virtual_environment(venv_name)

if __name__ == "__main__":
    main()