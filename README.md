# ⚙️ LeetCode Agent – Backend  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)  
![Supabase](https://img.shields.io/badge/Supabase-Database-black?logo=supabase)  
![Railway](https://img.shields.io/badge/Hosted-Railway-purple?logo=railway)  
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)  

## 🚀 Overview  
LeetCode Agent Backend powers the logic behind the **LeetCode Agent Chrome Extension**.  
It provides APIs to:  
- 🔍 Analyze user’s GitHub repo and solved problems  
- 🧩 Recommend the next LeetCode problem (by topic/difficulty)  
- 📊 Track solved problems per category  
- 🔗 Auto-push solved problems into GitHub with proper structure  

---

- **Frontend** – Chrome extension UI built with React, Vite, and Tailwind.  
  👉 [LeetCode Agent Frontend](https://github.com/<your-username>/LeetCode-Agent-UI)  
- **Backend (this repo)** – FastAPI service for repo analysis, recommendations, and GitHub integration.  
## My LeetCode Progress

<!-- LEETCODE-AGENT:START -->
Here will be your progress stats…
<!-- LEETCODE-AGENT:END -->
## Next sections…
## 📁 Project Structure

```
leetcode-agent-backend/
│
├── 📁 app/
│   ├── 📁 deps/
│   │   └── 🔐 auth_deps.py          # Authentication dependencies
│   ├── 📁 routers/
│   │   ├── 🔑 auth.py               # Authentication routes
│   │   ├── 🐙 github.py             # GitHub integration routes
│   │   └── 📚 repos.py              # Repository management routes
│   ├── 📁 services/
│   │   ├── 💾 db_service.py         # Database operations
│   │   ├── 🐙 github_service.py     # GitHub API interactions
│   │   └── 📊 repo_analyzer.py      # Repository analysis logic
│   ├── 📁 utils/
│   │   ├── 🔒 security.py           # Encryption/decryption utilities
│   │   └── 🌐 github_client.py      # GitHub GraphQL client
│   ├── 🗄️ database.py               # Database configuration
│   └── 📋 models.py                 # SQLAlchemy models
│
├── 📁 coral/                        # Coral MCP integration
├── 🐳 main.py                       # FastAPI application entry point
├── 📋 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git ignore rules
└── 📜 LICENSE                       # MIT License
```

---


## 📡 API Documentation

### 🔐 Authentication Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/auth/github` | Initiate GitHub OAuth flow | ❌ |
| `GET` | `/auth/callback` | Handle GitHub OAuth callback | ❌ |
| `GET` | `/auth/me?username={username}` | Get user authentication status | ❌ |

### 🐙 GitHub Integration Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/github/tree` | Get repository tree structure | ✅ |
| `GET` | `/github/commits` | Get commit history for a path | ✅ |
| `GET` | `/github/repos` | List user repositories | ✅ |
| `POST` | `/github/select_repo` | Select repository for LeetAgent | ✅ |

#### Example: Repository Tree Analysis
```bash
GET /github/tree?owner=abubakar2029&repo=leetcode-data-structures-and-algorithms&branch=main&save=true
```

#### Example: Commit History
```bash
GET /github/commits?owner=abubakar2029&repo=my-repo&path=src/algorithms&branch=main&last=10
```
---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (or Supabase)
- GitHub OAuth App
- Environment variables set up

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/leetcode-agent-backend.git
   cd leetcode-agent-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---
## 🌐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/leetcode_agent

# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_TOKEN=your_personal_access_token

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256

# Security
ENCRYPTION_KEY=your-32-byte-base64-encryption-key

# Extension Configuration
EXTENSION_REDIRECT=your-chrome-extension-id
```

### 🔑 Getting GitHub Credentials

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:8000/auth/callback`
4. Generate a Personal Access Token with `repo` and `user:email` scopes

### 🛡️ Generating Encryption Key

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Use this in ENCRYPTION_KEY
```

---


## 📜 License  
This project is licensed under the [MIT License](./LICENSE) © 2025 Muhammad Abu Bakar

---

<div align="center">

**⭐ Star this repository if you find it helpful! ⭐**

[🔝 Back to top](#-leetcode-agent-backend)

</div>
