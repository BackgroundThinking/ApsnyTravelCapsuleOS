# Automated Update Workflow (`/autoupdate`)

This document explains the automated update workflow for the **ApsnyTravelCapsuleOS** repository, triggered by the `/autoupdate` command. This system allows for on-demand, AI-driven improvements to the project.

---

## 🚀 The `/autoupdate` Command

The `/autoupdate` command is a powerful tool that allows you to trigger the AI agents to perform a single improvement cycle on the repository. When you type `/autoupdate` in a GitHub issue or comment, the system will:

1.  **Acknowledge the command:** The AI will confirm that it has received the command and is taking control.
2.  **Initiate an improvement cycle:** An AI agent will be assigned to perform a single, small action to improve the repository.
3.  **Report back:** Once the cycle is complete, the agent will report back with the action it took and the outcome.

---

## 🔄 The Improvement Cycle

Each `/autoupdate` command triggers a single **improvement cycle**. A cycle is a small, self-contained action that improves the repository in some way. The goal is to make continuous, incremental progress.

### Cycle Workflow

1.  **Task Identification:** The assigned AI agent scans the repository to identify a single, high-priority task based on its role (e.g., add a test, improve documentation, refactor a function).

2.  **Deep Thinking:** The agent enters a "deep-thinking" mode to analyze the task and formulate a plan. This involves:
    - Understanding the context of the code or document.
    - Considering the impact of the change.
    - Formulating the exact code or text to be written.

3.  **Action Execution:** The agent executes the planned action. This could be:
    - Writing a new file.
    - Editing an existing file.
    - Running a validation script.

4.  **Committing the Change:** The agent commits the change to the repository with a descriptive commit message.

5.  **Reporting:** The agent reports back in the original GitHub issue or comment with a summary of the action taken and a link to the commit.

### Example Cycle

> **User:** `/autoupdate`
>
> **AI Agent:** "Understood! I will now perform one improvement cycle."
>
> _Agent identifies that the `get_capsule_by_id` function in `data.ts` is missing a docstring._
>
> _Agent enters deep-thinking mode and formulates the docstring._
>
> _Agent edits `data.ts` to add the docstring._
>
> _Agent commits the change with the message: `docs: add docstring for get_capsule_by_id`_
>
> **AI Agent:** "✅ **Cycle Complete:** I have added a docstring to the `get_capsule_by_id` function in `client/src/lib/data.ts`. See commit `[commit_hash]`."

---

## 💡 How to Use `/autoupdate`

### General Improvements

To trigger a general improvement cycle, simply type:

```
/autoupdate
```

An available agent will pick a task based on its role and the current state of the repository.

### Targeted Improvements

You can also suggest a specific area for improvement:

```
/autoupdate focus on improving test coverage for the search module
```

In this case, the **Tester** agent will be assigned to the task and will focus on adding tests to the `client/src/lib/search.ts` file.

---

## 🧬 Connection to AI Agents Framework

The `/autoupdate` command is the manual trigger for the AI agents described in the [**AGENTS.md**](AGENTS.md) framework. The agents, their roles, and their operational cycle are all defined in that document.

---

## 📄 License

This automated update workflow is part of the **ApsnyTravelCapsuleOS** project and is licensed under the MIT License.

---

**Status:** ✅ **Workflow Active**
**Version:** v1.0
**Last Updated:** December 2, 2025
