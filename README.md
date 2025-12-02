# ApsnyTravelCapsuleOS v0.0.1

![GitHub last commit](https://img.shields.io/github/last-commit/BackgroundThinking/ApsnyTravelCapsuleOS) ![GitHub repo size](https://img.shields.io/github/repo-size/BackgroundThinking/ApsnyTravelCapsuleOS) ![GitHub license](https://img.shields.io/github/license/BackgroundThinking/ApsnyTravelCapsuleOS) ![GitHub issues](https://img.shields.io/github/issues/BackgroundThinking/ApsnyTravelCapsuleOS)

**ApsnyTravelCapsuleOS** is a sophisticated, enterprise-grade web application for exploring winter tourism in Abkhazia and Sochi. It is built on the **CapsuleOS** architecture, a modern, high-performance static web application framework.

![ApsnyTravel Hero](/client/public/images/hero-winter-ritsa.jpg)

## 🚀 Key Features

- **Dynamic Content:** The application is powered by a sophisticated algorithm that synchronizes content with the live ApsnyTravel.ru website.
- **High Performance:** The application is built with a modern, high-performance static web application framework that ensures blazing fast performance.
- **Enterprise-Grade:** The application is built with enterprise-grade features, including a comprehensive documentation suite, Docker containerization, and a GitHub Actions CI/CD pipeline.
- **Comprehensive Documentation:** The project includes a comprehensive documentation suite with 15+ guides covering all aspects of the project.

## 🛠️ Tech Stack

- **Frontend:** React 19, TypeScript 5.6, Vite 7, TailwindCSS
- **Backend (Algorithm):** Python 3.11, Pydantic, Requests
- **DevOps:** Docker, GitHub Actions, Nginx
- **Testing:** Vitest, Pydantic validation
- **Documentation:** Markdown

## 📖 Documentation

The project includes a comprehensive documentation suite with 15+ guides covering all aspects of the project, including deployment, operations, security, API documentation, algorithm documentation, testing, contribution guidelines, and troubleshooting.

Key documents:
- [**DEPLOYMENT.md**](DEPLOYMENT.md) - How to deploy the application
- [**OPERATIONS_MANUAL.md**](OPERATIONS_MANUAL.md) - How to operate and maintain
- [**ALGORITHM_DEPLOYMENT.md**](ALGORITHM_DEPLOYMENT.md) - How to run the synchronization algorithm
- [**SECURITY.md**](SECURITY.md) - Security best practices

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS.git
    cd ApsnyTravelCapsuleOS
    ```

2.  **Install dependencies:**
    ```bash
    pnpm install
    ```

3.  **Run the content synchronization algorithm:**
    ```bash
    python3 scripts/sync-with-apsnytravel.py
    ```

4.  **Start the development server:**
    ```bash
    pnpm dev
    ```

## 🤝 Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
