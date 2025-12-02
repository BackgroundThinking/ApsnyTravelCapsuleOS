# Quick Start Guide

Get up and running with ApsnyTravelCapsuleOS in 5 minutes!

## Prerequisites

Ensure you have the following installed on your system:

- Node.js 18 or higher
- Python 3.11 or higher
- pnpm (or npm/yarn)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS.git
cd ApsnyTravelCapsuleOS
```

## Step 2: Install Dependencies

```bash
pnpm install
```

## Step 3: Synchronize Content

Run the algorithm to fetch and process content from ApsnyTravel.ru:

```bash
python3 scripts/sync-with-apsnytravel.py
```

This will generate the necessary JSON files in the `client/public/` directory.

## Step 4: Start Development Server

```bash
pnpm dev
```

The application will be available at `http://localhost:5173`.

## Step 5: Build for Production

```bash
pnpm build
```

The production build will be created in the `dist/` directory.

## Next Steps

- Read the [DEPLOYMENT.md](../DEPLOYMENT.md) guide to deploy to production
- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) guide to contribute
- Review the [ALGORITHM_DEPLOYMENT.md](../ALGORITHM_DEPLOYMENT.md) to understand the algorithm
- See [DEVELOPMENT.md](DEVELOPMENT.md) for advanced development setup

## Troubleshooting

If you encounter any issues, please refer to the [ERROR_HANDLING.md](../ERROR_HANDLING.md) guide or check the GitHub issues.

---

**Happy coding!** 🚀
