import streamlit as st
import requests
import base64

# GitHub API URL
GITHUB_API_URL = "https://github.com/codingacharya/startupanalysis.git"

# Streamlit App
st.set_page_config(page_title="Startup company analysis", layout="wide")

st.title("🔗 GitHub Python Project Explorer")

# Input: GitHub Username & Repository Name
username = st.text_input("Enter GitHub Username:", value="streamlit")
repo_name = st.text_input("Enter Repository Name:", value="streamlit")

if username and repo_name:
    repo_url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}"
    response = requests.get(repo_url)

    if response.status_code == 200:
        repo_data = response.json()
        st.subheader(f"📂 Repository: {repo_data['name']}")
        st.write(f"**Description:** {repo_data['description']}")
        st.write(f"⭐ Stars: {repo_data['stargazers_count']} | 🍴 Forks: {repo_data['forks_count']}")
        st.write(f"🔗 [View on GitHub]({repo_data['html_url']})")

        # Fetch repository contents
        contents_url = f"{repo_url}/contents"
        contents_response = requests.get(contents_url)
        
        if contents_response.status_code == 200:
            files = contents_response.json()
            python_files = [file for file in files if file["name"].endswith(".py")]

            if python_files:
                st.subheader("📜 Python Files in Repository")
                selected_file = st.selectbox("Select a Python file:", [file["name"] for file in python_files])

                # Fetch file content
                if selected_file:
                    file_data = next(file for file in python_files if file["name"] == selected_file)
                    file_response = requests.get(file_data["download_url"])
                    
                    if file_response.status_code == 200:
                        file_content = file_response.text
                        st.code(file_content, language="python")
                    else:
                        st.error("Could not fetch file content.")
            else:
                st.warning("No Python files found in this repository.")
        else:
            st.error("Failed to fetch repository contents.")
    else:
        st.error("Repository not found. Please check the username and repository name.")

