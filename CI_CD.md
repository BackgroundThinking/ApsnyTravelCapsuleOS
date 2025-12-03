# CI/CD Documentation

## ApsnyTravelCapsuleOS Continuous Integration & Deployment

**Version**: 1.0  
**Last Updated**: December 2, 2025

---

## Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) infrastructure for ApsnyTravelCapsuleOS, including workflows, configuration, and best practices.

---

## Table of Contents

1. [Architecture](#architecture)
2. [Workflows](#workflows)
3. [Configuration](#configuration)
4. [Branch Protection](#branch-protection)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Future Enhancements](#future-enhancements)

---

## Architecture

### CI/CD Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   PR Event   │    │  Push Event  │    │ Manual Run   │ │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘ │
│         │                   │                    │          │
│         └───────────────────┴────────────────────┘          │
│                            │                                 │
│                            ▼                                 │
│              ┌─────────────────────────┐                    │
│              │  GitHub Actions Runner  │                    │
│              └─────────────────────────┘                    │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐            │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │  Test Job   │   │  Lint Job   │   │  Build Job  │     │
│  └─────────────┘   └─────────────┘   └─────────────┘     │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │  ✅ Pass    │   │  ✅ Pass    │   │  ✅ Pass    │     │
│  │  ❌ Fail    │   │  ❌ Fail    │   │  ❌ Fail    │     │
│  └─────────────┘   └─────────────┘   └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **GitHub Actions**: CI/CD platform
2. **Workflows**: Automated job definitions
3. **Runners**: Ubuntu-based execution environment
4. **Artifacts**: Build outputs and reports
5. **Status Checks**: Pass/fail indicators

---

## Workflows

### 1. Test Workflow (`.github/workflows/test.yml`)

**Purpose**: Execute all tests and generate coverage reports

**Triggers**:

- Pull requests to any branch
- Push to `main` branch
- Manual workflow dispatch

**Steps**:

1. Checkout code
2. Setup Node.js 22
3. Setup pnpm 10
4. Cache pnpm store
5. Install dependencies
6. Run tests with coverage
7. Upload coverage artifacts
8. Comment coverage on PR (if PR event)

**Outputs**:

- Test results (pass/fail)
- Coverage report (HTML + JSON)
- PR comment with coverage summary

**Duration**: ~1-2 minutes

---

### 2. Lint Workflow (`.github/workflows/lint.yml`)

**Purpose**: Enforce code quality and type safety

**Triggers**:

- Pull requests to any branch
- Push to `main` branch
- Manual workflow dispatch

**Jobs**:

#### Job 1: Format Check

- Runs Prettier format check
- Fails if code is not formatted

#### Job 2: Type Check

- Runs TypeScript compiler (noEmit)
- Fails if type errors exist

**Duration**: ~1 minute

---

### 3. Build Workflow (`.github/workflows/build.yml`)

**Purpose**: Verify production build succeeds

**Triggers**:

- Pull requests to any branch
- Push to `main` branch
- Manual workflow dispatch

**Steps**:

1. Checkout code
2. Setup Node.js 22 and Python 3.11
3. Setup pnpm 10
4. Install dependencies
5. Run production build
6. Check build output
7. Check bundle size
8. Upload build artifacts (main branch only)

**Outputs**:

- Build success/failure
- Bundle size report
- Build artifacts (dist/)

**Duration**: ~2-3 minutes

---

## Configuration

### Workflow Permissions

```yaml
permissions:
  contents: read # Read repository contents
  pull-requests: write # Comment on PRs
  checks: write # Update status checks
```

### Caching Strategy

All workflows use pnpm store caching:

```yaml
- name: Setup pnpm cache
  uses: actions/cache@v4
  with:
    path: ${{ env.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-store-
```

**Benefits**:

- Faster dependency installation (30s → 5s)
- Reduced network usage
- Consistent dependency versions

### Environment Variables

| Variable         | Value | Usage           |
| ---------------- | ----- | --------------- |
| `NODE_VERSION`   | 22    | Node.js version |
| `PNPM_VERSION`   | 10    | pnpm version    |
| `PYTHON_VERSION` | 3.11  | Python version  |

---

## Branch Protection

### Recommended Settings

Navigate to: **Settings** → **Branches** → **Branch protection rules** → **main**

#### Required Status Checks

- ✅ `Test / test`
- ✅ `Lint / lint`
- ✅ `Lint / type-check`
- ✅ `Build / build`

#### Additional Settings

- ✅ Require branches to be up to date before merging
- ✅ Require pull request before merging
- ✅ Require 1 approval
- ✅ Dismiss stale reviews
- ✅ Require review from code owners (optional)

#### Merge Options

- ✅ Allow squash merging
- ✅ Allow merge commits
- ❌ Allow rebase merging (optional)
- ✅ Automatically delete head branches

---

## Monitoring

### Viewing Workflow Runs

1. Navigate to **Actions** tab
2. Select workflow (Test, Lint, or Build)
3. View run history and logs

### Coverage Reports

#### Viewing in PR

- Coverage summary is automatically commented on PRs
- Click link to view detailed report

#### Downloading Artifacts

1. Go to workflow run
2. Scroll to **Artifacts** section
3. Download `coverage-report`
4. Open `coverage/index.html` locally

### Status Badges

Add to README.md:

```markdown
![Test](https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS/actions/workflows/lint.yml/badge.svg)
![Build](https://github.com/BackgroundThinking/ApsnyTravelCapsuleOS/actions/workflows/build.yml/badge.svg)
```

---

## Troubleshooting

### Common Issues

#### Workflow Fails on Dependency Installation

**Symptom**: `pnpm install` fails  
**Cause**: Corrupted cache or lockfile mismatch  
**Solution**:

```bash
# Locally
rm -rf node_modules pnpm-lock.yaml
pnpm install
git add pnpm-lock.yaml
git commit -m "fix: update lockfile"
git push
```

#### Tests Pass Locally But Fail in CI

**Symptom**: Tests fail in CI but pass locally  
**Cause**: Environment differences  
**Solution**:

- Check Node.js version matches (22)
- Ensure dependencies are committed
- Review workflow logs for errors

#### Coverage Report Not Generated

**Symptom**: No coverage artifact uploaded  
**Cause**: Coverage provider not installed  
**Solution**:

```bash
pnpm add -D @vitest/coverage-v8
git add package.json pnpm-lock.yaml
git commit -m "fix: add coverage provider"
```

#### Build Fails with Python Error

**Symptom**: `generate_sitemap.py` fails  
**Cause**: Python dependencies missing  
**Solution**:

- Ensure Python 3.11 is specified in workflow
- Add Python dependency installation if needed

### Debugging Workflows

#### Enable Debug Logging

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add repository variable:
   - Name: `ACTIONS_STEP_DEBUG`
   - Value: `true`

#### Re-run Failed Jobs

1. Navigate to failed workflow run
2. Click **Re-run jobs** → **Re-run failed jobs**

#### View Detailed Logs

1. Click on failed job
2. Expand failed step
3. Review error messages and stack traces

---

## Future Enhancements

### Phase 2: Enhanced Reporting

- [ ] Coverage badges in README
- [ ] Detailed PR comments with file-level coverage
- [ ] Historical coverage trends
- [ ] Performance metrics tracking

### Phase 3: Advanced Testing

- [ ] E2E testing workflow (Playwright)
- [ ] Visual regression testing
- [ ] Performance testing
- [ ] Accessibility testing

### Phase 4: Deployment Automation

- [ ] Automated deployment to staging
- [ ] Automated deployment to production
- [ ] Rollback capabilities
- [ ] Deployment notifications

### Phase 5: Quality Gates

- [ ] Enforce coverage thresholds (80%+)
- [ ] Bundle size limits
- [ ] Performance budgets
- [ ] Security scanning (Dependabot, CodeQL)

---

## Best Practices

### 1. Keep Workflows Fast

- Use caching aggressively
- Run jobs in parallel when possible
- Optimize test execution time
- Skip unnecessary steps

### 2. Fail Fast

- Run fastest checks first (lint, type-check)
- Use `fail-fast: false` for parallel jobs
- Provide clear error messages

### 3. Maintain Workflows

- Review workflow runs regularly
- Update actions to latest versions
- Clean up old artifacts
- Monitor execution time trends

### 4. Security

- Use official actions from trusted sources
- Pin action versions (e.g., `@v4`)
- Limit workflow permissions
- Never commit secrets to workflows

### 5. Documentation

- Keep this document updated
- Document workflow changes in PRs
- Add comments to complex workflow steps
- Maintain changelog

---

## Resources

### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Vitest CI Integration](https://vitest.dev/guide/ci.html)

### Tools

- [act](https://github.com/nektos/act) - Run workflows locally
- [actionlint](https://github.com/rhysd/actionlint) - Lint workflow files

### Examples

- `.github/workflows/test.yml` - Test workflow
- `.github/workflows/lint.yml` - Lint workflow
- `.github/workflows/build.yml` - Build workflow

---

## Support

### Getting Help

1. **Check Workflow Logs**: Most issues are evident in logs
2. **Review This Documentation**: Common issues are documented
3. **GitHub Discussions**: Ask the community
4. **GitHub Issues**: Report bugs or feature requests

### Reporting Issues

When reporting CI/CD issues, include:

- Workflow run URL
- Error messages from logs
- Steps to reproduce
- Expected vs actual behavior

---

## Changelog

### Version 1.0 (December 2, 2025)

- Initial CI/CD infrastructure
- Test workflow with coverage
- Lint workflow with type checking
- Build verification workflow
- Comprehensive documentation

---

**Maintained by**: ApsnyTravelCapsuleOS Team  
**Last Review**: December 2, 2025
