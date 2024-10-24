# .github/release.py

import json
import subprocess
import os

# Load release.json file
with open('release.json', 'r') as f:
    release_data = json.load(f)

# Iterate over projects and update submodules to the specified tag
for project_info in release_data['projects']:
    project_name = project_info['project']
    project_tag = project_info['tag']
    
    # Assuming the submodule path is the same as the project name
    submodule_path = os.path.join(os.getcwd(), project_name)
    
    if os.path.exists(submodule_path):
        print(f"Updating submodule: {project_name} to tag: {project_tag}")
        
        # Change to the submodule directory
        os.chdir(submodule_path)
        
        # Fetch all tags for the submodule
        subprocess.run(['git', 'fetch', '--tags'], check=True)
        
        # Checkout the specific tag
        subprocess.run(['git', 'checkout', project_tag], check=True)
        
        # Move back to the main repository directory
        os.chdir('..')
        
        # Update the submodule's state in the main repo
        subprocess.run(['git', 'add', project_name], check=True)
    else:
        print(f"Submodule path {submodule_path} does not exist. Please initialize the submodule first.")

# Commit the changes in the main repository
subprocess.run(['git', 'commit', '-m', f"Update submodules based on {release_data['release']}"], check=True)

# Optionally, you can push the changes
# subprocess.run(['git', 'push'], check=True)
