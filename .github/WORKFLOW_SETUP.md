# GitHub Actions Workflow Setup Guide

## Overview

This directory contains GitHub Actions workflow templates that implement comprehensive CI/CD automation for ApsnyTravelCapsuleOS. Due to GitHub App security restrictions, these workflows cannot be automatically activated and must be manually enabled.

## Quick Setup

### Step 1: Activate Workflows

Copy the workflow templates to the workflows directory:

```bash
cp .github/workflow-templates/*.yml .github/workflows/
git add .github/workflows/*.yml
git commit -m "ci: activate GitHub Actions workflows"
git push origin main
```

### Step 2: Configure Repository Settings

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
3. Under **Workflow permissions**, enable:
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### Step 3: Configure Branch Protection (Recommended)

1. Go to **Settings** → **Branches**
2. Click **Add rule** for `main` branch
3. Enable:
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
4. Select required status checks:
   - ✅ `Test / test`
   - ✅ `Lint / lint`
   - ✅ `Lint / type-check`
   - ✅ `Build / build`
5. Click **Create** or **Save changes**

## Available Workflows

### 1. Test Workflow (`test.yml`)

**Purpose**: Run all tests with coverage reporting

**Triggers**:
- Pull requests to any branch
- Push to main branch
- Manual workflow dispatch

**Features**:
- Executes all Vitest tests
- Generates coverage reports
- Uploads coverage artifacts
- Comments coverage summary on PRs

### 2. Lint Workflow (`lint.yml`)

**Purpose**: Enforce code quality standards

**Triggers**:
- Pull requests to any branch
- Push to main branch
- Manual workflow dispatch

**Features**:
- Prettier format checking
- TypeScript type checking
- Parallel job execution

### 3. Build Workflow (`build.yml`)

**Purpose**: Verify production build

**Triggers**:
- Pull requests to any branch
- Push to main branch
- Manual workflow dispatch

**Features**:
- Production build verification
- Bundle size checking
- Build artifact upload (main branch only)

## Verification

After activating workflows, verify they work:

1. Go to **Actions** tab
2. You should see the three workflows listed
3. Click **Run workflow** on any workflow to test manually
4. Create a test PR to verify automatic execution

## Troubleshooting

### Workflows Don't Appear

**Cause**: Workflows not in `.github/workflows/` directory  
**Solution**: Ensure you copied files to the correct location

### Workflows Fail on First Run

**Cause**: Missing dependencies or configuration  
**Solution**: Check workflow logs for specific errors

### Coverage Report Not Posted

**Cause**: Missing PR write permissions  
**Solution**: Enable "Allow GitHub Actions to create and approve pull requests" in settings

## Documentation

For detailed information, see:
- [TESTING.md](../../TESTING.md) - Testing guide
- [CI_CD.md](../../CI_CD.md) - CI/CD documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

If you encounter issues:
1. Check workflow logs in the Actions tab
2. Review the troubleshooting section in CI_CD.md
3. Open an issue on GitHub

---

**Note**: This manual activation step is a security feature to prevent unauthorized workflow modifications. Once activated, workflows will run automatically on every PR and push.
