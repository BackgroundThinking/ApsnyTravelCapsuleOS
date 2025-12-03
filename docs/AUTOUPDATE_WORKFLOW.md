# Auto-Update GitHub Actions Workflow Setup

This document provides instructions for setting up the GitHub Actions workflow for the automated update system.

## Overview

The auto-update system can be automated using GitHub Actions to run the agent system on a schedule or when changes are pushed to the repository.

## Workflow Implementation

### Script Location

The autoupdate script is located at `scripts/autoupdate.js` and can be run locally or via GitHub Actions.

### Local Usage

```bash
# Run all agents
node scripts/autoupdate.js --agent=all

# Run a specific agent
node scripts/autoupdate.js --agent=architect
node scripts/autoupdate.js --agent=documenter
node scripts/autoupdate.js --agent=tester
node scripts/autoupdate.js --agent=security
node scripts/autoupdate.js --agent=janitor
```

## GitHub Actions Workflow

Due to GitHub App permissions, the workflow file needs to be created manually in the repository. A template is provided at `.github/autoupdate.workflow.yml`.

### File Location

Create `.github/workflows/autoupdate.yml` (copy from `.github/autoupdate.workflow.yml`)

### Workflow Content

```yaml
name: Auto Update

on:
  # Trigger on push to main branch
  push:
    branches:
      - main
  
  # Trigger on schedule (daily at 2 AM UTC)
  schedule:
    - cron: '0 2 * * *'
  
  # Allow manual trigger
  workflow_dispatch:
    inputs:
      agent:
        description: 'Specific agent to run (architect, documenter, tester, security, janitor, or all)'
        required: false
        default: 'all'

jobs:
  autoupdate:
    runs-on: ubuntu-latest
    
    permissions:
      contents: write
      pull-requests: write
      issues: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      - name: Configure Git
        run: |
          git config --global user.name "ApsnyTravel AutoUpdate Bot"
          git config --global user.email "autoupdate@apsnytravel.com"
      
      - name: Run Auto Update
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          AGENT_MODE: ${{ github.event.inputs.agent || 'all' }}
        run: |
          echo "Running auto-update with agent mode: $AGENT_MODE"
          mkdir -p logs
          node scripts/autoupdate.js --agent=$AGENT_MODE --config=.autoupdate.yml
      
      - name: Commit and Push Changes
        run: |
          if [[ -n $(git status -s) ]]; then
            echo "Changes detected, committing..."
            git add .
            COMMIT_MSG="chore: automated update by autoupdate workflow"
            git commit -m "$COMMIT_MSG"
            git push origin main
            echo "Changes pushed successfully"
          else
            echo "No changes to commit"
          fi
      
      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: autoupdate-logs
          path: |
            .autoupdate.log
            .autoupdate_audit.log
            logs/
          retention-days: 30
      
      - name: Create Issue on Failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const title = '🚨 Auto Update Workflow Failed';
            const body = `The auto-update workflow failed on ${new Date().toISOString()}.
            
            **Workflow Run:** ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
            
            Please review the logs and take appropriate action.`;
            
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: title,
              body: body,
              labels: ['autoupdate', 'bug']
            });
```

## Setup Instructions

### Step 1: Create the Workflow File

**Option A: Via GitHub Web Interface**

1. Navigate to your repository on GitHub
2. Go to the `.github/` directory
3. Open the file `autoupdate.workflow.yml`
4. Copy the entire contents
5. Navigate to `.github/workflows/` (create the directory if needed)
6. Create a new file named `autoupdate.yml`
7. Paste the copied content
8. Commit the file directly to the `main` branch

**Option B: Via Command Line**

```bash
cp .github/autoupdate.workflow.yml .github/workflows/autoupdate.yml
git add .github/workflows/autoupdate.yml
git commit -m "chore: enable auto-update GitHub Actions workflow"
git push origin main
```

### Step 2: Enable GitHub Actions

1. Go to your repository **Settings**
2. Navigate to **Actions** → **General**
3. Ensure that **Allow all actions and reusable workflows** is selected
4. Under **Workflow permissions**, select **Read and write permissions**
5. Check **Allow GitHub Actions to create and approve pull requests**

### Step 3: Test the Workflow

1. Go to the **Actions** tab in your repository
2. Select the **Auto Update** workflow
3. Click **Run workflow**
4. Select an agent to run (or leave as "all")
5. Click **Run workflow** to start

### Step 4: Monitor Execution

1. View the workflow run in the **Actions** tab
2. Check the logs for each step
3. Download artifacts to review detailed logs
4. Verify that changes are committed if any were made

## Workflow Triggers

The workflow can be triggered in three ways:

### 1. Manual Trigger

- Go to **Actions** → **Auto Update** → **Run workflow**
- Select which agent(s) to run
- Useful for on-demand improvements

### 2. Push to Main

- Automatically runs when changes are pushed to `main`
- Validates changes and suggests improvements
- Helps maintain code quality continuously

### 3. Scheduled Execution

- Runs daily at 2 AM UTC by default
- Can be customized by editing the cron expression
- Performs regular maintenance and improvements

## Configuration

The workflow integrates with the existing `.autoupdate.yml` configuration file. Key settings include:

- **Agent Settings**: Enable/disable agents, set priorities
- **Improvement Cycle**: Control pace of changes
- **Safety Restrictions**: Protect critical files
- **Monitoring**: Track metrics and performance

## Troubleshooting

### Workflow Not Appearing

- Ensure the workflow file is in `.github/workflows/`
- Check that the file has a `.yml` or `.yaml` extension
- Verify that Actions are enabled in repository settings

### Permission Errors

- Check workflow permissions in repository settings
- Ensure **Read and write permissions** are enabled
- Verify that the workflow has `contents: write` permission

### Script Errors

- Review logs in the Actions tab
- Download artifacts for detailed error messages
- Test the script locally to reproduce issues

## Security Considerations

1. **Token Security**: Uses `GITHUB_TOKEN` which is automatically scoped
2. **Protected Paths**: Configuration prevents modification of critical files
3. **Change Limits**: Maximum files and lines per cycle are enforced
4. **Audit Trail**: All actions are logged for review

## Integration with Existing System

This workflow integrates with:

- `.autoupdate.yml` - Configuration file
- `scripts/autoupdate.js` - Agent implementation
- `docs/AUTOUPDATE.md` - User documentation
- `docs/AGENTS.md` - Agent framework documentation

## Best Practices

1. **Start Small**: Begin with manual triggers to test the system
2. **Monitor Regularly**: Check workflow runs weekly
3. **Review Changes**: Audit automated commits periodically
4. **Adjust Configuration**: Fine-tune agent settings based on results
5. **Keep Updated**: Update workflow actions and dependencies regularly

## Related Documentation

- [Auto-Update System](AUTOUPDATE.md) - User-facing documentation
- [AI Agents Framework](AGENTS.md) - Agent system design
- [Contributing Guide](../CONTRIBUTING.md) - Contribution guidelines
- [Configuration Reference](../.autoupdate.yml) - Full configuration options
