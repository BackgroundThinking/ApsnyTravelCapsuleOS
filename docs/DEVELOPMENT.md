# Development Guide

This guide covers the development setup, workflow, and best practices for contributing to ApsnyTravelCapsuleOS.

## Development Environment Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm
- Git

### Installation

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS.git
cd ApsnyTravelCapsuleOS
pnpm install
```

2. Install Python dependencies for the algorithm:

```bash
cd algorithm
pip install -r requirements.txt
cd ..
```

3. Set up environment variables (optional):

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development Workflow

### Starting the Development Server

```bash
pnpm dev
```

The application will be available at `http://localhost:5173` with hot module replacement enabled.

### Running Tests

Run the test suite:

```bash
pnpm test
```

Run tests in watch mode:

```bash
pnpm test:watch
```

### Type Checking

Check TypeScript types:

```bash
pnpm check
```

### Building for Production

Create a production build:

```bash
pnpm build
```

### Validating Content

Validate the capsules data:

```bash
python3 scripts/validate-capsules.py
```

### Running the Algorithm

Synchronize content with ApsnyTravel.ru:

```bash
python3 scripts/sync-with-apsnytravel.py
```

## Project Structure

The project is organized as follows:

- `algorithm/` - Python modules for the synchronization algorithm
- `client/` - React frontend application
- `scripts/` - Utility scripts for content management and deployment
- `docs/` - Documentation files
- `.github/` - GitHub configuration (workflows, templates)

## Code Style

The project follows these code style guidelines:

- **TypeScript/JavaScript:** Use ESLint and Prettier for linting and formatting
- **Python:** Follow PEP 8 style guide
- **CSS:** Use Tailwind CSS utility classes

To format code:

```bash
pnpm format
```

## Git Workflow

1. Create a feature branch from `main`:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit with descriptive messages:

```bash
git commit -m "feat: add new feature"
```

3. Push your branch and create a pull request:

```bash
git push origin feature/your-feature-name
```

4. Wait for code review and address any feedback

5. Once approved, your PR will be merged into `main`

## Testing

All new features should include tests. Run the test suite before submitting a PR:

```bash
pnpm test
```

## Documentation

Update documentation when making changes:

- Update relevant `.md` files in the `docs/` directory
- Update the README.md if the changes affect the project overview
- Add comments to complex code sections

## Performance Optimization

When making changes, consider performance implications:

- Use React.memo for expensive components
- Implement code splitting for large modules
- Minimize bundle size with tree-shaking
- Use lazy loading for images and components

## Debugging

### Browser DevTools

Use the React DevTools and Redux DevTools browser extensions for debugging.

### Logging

Use the logger utility for structured logging:

```typescript
import { logger } from "@/lib/logger";

logger.info("Message", { context: "value" });
logger.error("Error occurred", { error: err });
```

### Python Debugging

Enable debug logging in the algorithm:

```bash
DEBUG=1 python3 scripts/sync-with-apsnytravel.py
```

## Deployment

For deployment instructions, see [DEPLOYMENT.md](../DEPLOYMENT.md).

## Getting Help

- Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Review existing issues and discussions
- Ask questions in GitHub discussions
- Refer to the [ERROR_HANDLING.md](../ERROR_HANDLING.md) for troubleshooting

---

**Happy developing!** 🚀
