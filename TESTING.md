# Testing Guide

## ApsnyTravelCapsuleOS

**Version**: 1.0  
**Last Updated**: December 2, 2025

---

## Overview

This document provides comprehensive guidance on testing practices, running tests, writing new tests, and understanding the testing infrastructure for ApsnyTravelCapsuleOS.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Testing Philosophy](#testing-philosophy)
3. [Test Structure](#test-structure)
4. [Running Tests](#running-tests)
5. [Writing Tests](#writing-tests)
6. [Coverage](#coverage)
7. [CI/CD Integration](#cicd-integration)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Install Dependencies

```bash
pnpm install
```

### Run All Tests

```bash
pnpm test
```

### Run Tests in Watch Mode

```bash
pnpm test:watch
```

### Generate Coverage Report

```bash
pnpm test:coverage
```

---

## Testing Philosophy

Our testing approach follows these principles:

1. **Comprehensive Coverage**: Aim for 80%+ code coverage
2. **Fast Execution**: Tests should run quickly (< 5 seconds total)
3. **Isolated Tests**: Each test should be independent
4. **Clear Assertions**: Tests should clearly express intent
5. **Maintainable**: Tests should be easy to understand and modify

### Testing Pyramid

```
        ┌─────────────┐
        │   E2E Tests │  (Future)
        │   (Manual)  │
        └─────────────┘
       ┌───────────────┐
       │ Integration   │  (Future)
       │     Tests     │
       └───────────────┘
      ┌─────────────────┐
      │   Unit Tests    │  (Current Focus)
      │  (Vitest)       │
      └─────────────────┘
```

---

## Test Structure

### Directory Organization

```
client/src/
├── __tests__/              # Test files
│   ├── lib.data.test.ts    # Data layer tests
│   ├── lib.search.test.ts  # Search functionality tests
│   └── lib.logger.test.ts  # Logger utility tests
├── components/             # React components
├── lib/                    # Library modules
│   ├── data.ts
│   ├── search.ts
│   ├── logger.ts
│   ├── seo.ts
│   ├── jsonld.ts
│   └── utils.ts
└── pages/                  # Page components
```

### Test File Naming

- **Unit Tests**: `*.test.ts` or `*.test.tsx`
- **Integration Tests**: `*.integration.test.ts`
- **E2E Tests**: `*.e2e.test.ts` (future)

### Test Suite Organization

```typescript
describe("ModuleName - Feature", () => {
  // Setup
  beforeEach(() => {
    // Initialize test state
  });

  // Test cases
  it("should do something specific", () => {
    // Arrange
    const input = "test";

    // Act
    const result = functionUnderTest(input);

    // Assert
    expect(result).toBe("expected");
  });
});
```

---

## Running Tests

### Basic Commands

#### Run All Tests Once

```bash
pnpm test
```

#### Run Tests in Watch Mode (Development)

```bash
pnpm test:watch
```

#### Run Tests with Coverage

```bash
pnpm test:coverage
```

#### Run Tests with UI

```bash
pnpm test:ui
```

### Advanced Options

#### Run Specific Test File

```bash
pnpm test client/src/__tests__/lib.data.test.ts
```

#### Run Tests Matching Pattern

```bash
pnpm test --grep "search"
```

#### Run Tests in Specific Directory

```bash
pnpm test client/src/__tests__/
```

#### Run with Verbose Output

```bash
pnpm test --reporter=verbose
```

---

## Writing Tests

### Unit Test Example

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { myFunction } from "@/lib/myModule";

describe("MyModule - myFunction", () => {
  it("should return expected value for valid input", () => {
    const result = myFunction("input");
    expect(result).toBe("expected output");
  });

  it("should handle edge cases", () => {
    expect(myFunction("")).toBe("");
    expect(myFunction(null)).toBeNull();
  });

  it("should throw error for invalid input", () => {
    expect(() => myFunction(undefined)).toThrow();
  });
});
```

### Component Test Example (Future)

```typescript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MyComponent } from "@/components/MyComponent";

describe("MyComponent", () => {
  it("should render with props", () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText("Test")).toBeInTheDocument();
  });

  it("should handle user interaction", async () => {
    const { user } = render(<MyComponent />);
    await user.click(screen.getByRole("button"));
    expect(screen.getByText("Clicked")).toBeInTheDocument();
  });
});
```

### Mocking Example

```typescript
import { describe, it, expect, vi } from "vitest";

describe("Module with Dependencies", () => {
  it("should mock external dependency", () => {
    const mockFetch = vi.fn().mockResolvedValue({ data: "test" });
    global.fetch = mockFetch;

    // Test code that uses fetch
    expect(mockFetch).toHaveBeenCalled();
  });
});
```

---

## Coverage

### Coverage Configuration

Coverage is configured in `vitest.config.ts`:

```typescript
coverage: {
  provider: "v8",
  reporter: ["text", "json", "html", "lcov"],
  exclude: [
    "node_modules/",
    "dist/",
    "**/*.test.ts",
    "**/*.test.tsx",
    "**/*.config.ts"
  ],
  thresholds: {
    lines: 50,
    functions: 50,
    branches: 50,
    statements: 50
  }
}
```

### Viewing Coverage Reports

#### Terminal Output

```bash
pnpm test:coverage
```

#### HTML Report

```bash
pnpm test:coverage
open coverage/index.html
```

### Coverage Goals

| Metric     | Current | Target |
| ---------- | ------- | ------ |
| Lines      | ~20%    | 80%    |
| Functions  | ~20%    | 80%    |
| Branches   | ~15%    | 75%    |
| Statements | ~20%    | 80%    |

---

## CI/CD Integration

### Automated Testing

Tests run automatically on:

- **Pull Requests**: All tests must pass before merge
- **Push to Main**: Ensures main branch is always stable
- **Manual Trigger**: Can be run on-demand

### GitHub Actions Workflows

#### Test Workflow (`.github/workflows/test.yml`)

- Runs all tests with coverage
- Uploads coverage reports
- Comments coverage on PRs

#### Lint Workflow (`.github/workflows/lint.yml`)

- Checks code formatting
- Runs TypeScript type checking

#### Build Workflow (`.github/workflows/build.yml`)

- Verifies production build
- Checks bundle size

### Required Status Checks

Before merging a PR, these checks must pass:

- ✅ Test / test
- ✅ Lint / lint
- ✅ Lint / type-check
- ✅ Build / build

---

## Best Practices

### 1. Test Organization

**DO**:

- Group related tests in `describe` blocks
- Use clear, descriptive test names
- Follow Arrange-Act-Assert pattern

**DON'T**:

- Mix unrelated tests in one file
- Use vague test names like "it works"
- Test implementation details

### 2. Test Independence

**DO**:

- Each test should be self-contained
- Use `beforeEach` for setup
- Clean up after tests

**DON'T**:

- Depend on test execution order
- Share mutable state between tests
- Leave side effects

### 3. Assertions

**DO**:

- Use specific matchers (`toBe`, `toEqual`, `toContain`)
- Test one concept per test
- Include error messages for clarity

**DON'T**:

- Use generic matchers when specific ones exist
- Test multiple unrelated things in one test
- Forget to assert

### 4. Mocking

**DO**:

- Mock external dependencies
- Verify mock calls when relevant
- Restore mocks after tests

**DON'T**:

- Mock everything (test real code when possible)
- Forget to clean up mocks
- Over-specify mock behavior

### 5. Coverage

**DO**:

- Aim for high coverage (80%+)
- Focus on critical paths
- Test edge cases

**DON'T**:

- Aim for 100% at the expense of test quality
- Ignore uncovered code
- Write tests just for coverage

---

## Troubleshooting

### Common Issues

#### Tests Fail Locally But Pass in CI

**Cause**: Environment differences  
**Solution**:

```bash
# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
pnpm test
```

#### Coverage Report Not Generated

**Cause**: Missing coverage configuration  
**Solution**:

```bash
# Install coverage provider
pnpm add -D @vitest/coverage-v8
pnpm test:coverage
```

#### Tests Timeout

**Cause**: Async operations not handled properly  
**Solution**:

```typescript
// Use async/await
it("should handle async", async () => {
  const result = await asyncFunction();
  expect(result).toBe("value");
});
```

#### Mock Not Working

**Cause**: Mock not properly configured  
**Solution**:

```typescript
// Use vi.fn() for functions
const mockFn = vi.fn().mockReturnValue("value");

// Use vi.spyOn() for methods
vi.spyOn(console, "log").mockImplementation(() => {});
```

### Getting Help

1. **Check Vitest Documentation**: https://vitest.dev
2. **Search GitHub Issues**: Existing solutions may exist
3. **Ask in Discussions**: Community support
4. **Review Existing Tests**: Learn from examples

---

## Resources

### Documentation

- [Vitest Documentation](https://vitest.dev)
- [Testing Library](https://testing-library.com)
- [Jest Matchers](https://jestjs.io/docs/expect) (Vitest compatible)

### Tools

- **Vitest**: Test runner
- **jsdom**: DOM environment
- **@testing-library/react**: React testing utilities (future)

### Examples

- `client/src/__tests__/lib.data.test.ts` - Data layer tests
- `client/src/__tests__/lib.search.test.ts` - Search tests
- `client/src/__tests__/lib.logger.test.ts` - Logger tests

---

## Contributing

When contributing tests:

1. **Follow Conventions**: Match existing test style
2. **Write Clear Tests**: Tests should be self-documenting
3. **Maintain Coverage**: Don't decrease coverage
4. **Update Documentation**: Keep this guide current

---

## Changelog

### Version 1.0 (December 2, 2025)

- Initial testing guide
- Vitest configuration
- CI/CD integration
- Coverage tracking
- Best practices documentation

---

**Questions?** Open an issue or discussion on GitHub.
