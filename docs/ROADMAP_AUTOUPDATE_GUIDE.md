# ROADMAP & Autoupdate System - Complete Guide

**Version:** 1.0  
**Created:** December 2, 2025  
**Status:** Ready for Use

---

## Overview

The ROADMAP file integrated with the autoupdate system enables you to execute project tasks iteratively through the `/autoupdate` command. Tasks are executed sequentially in iteration cycles, not in parallel.

### Key Features

- **Iterative Execution:** Tasks broken into manageable iteration cycles
- **Sequential Processing:** One task at a time, not multithreaded
- **Autoupdate Integration:** Use `/autoupdate` to trigger next iteration
- **Progress Tracking:** Real-time status updates in ROADMAP
- **Flexible Timeline:** Adjust based on actual progress

---

## Quick Start

### View Current Status

```bash
python3 scripts/autoupdate_roadmap.py --status
```

Output shows:

- All phases and milestones
- Progress percentage for each milestone
- Current completion status

### View Next Task

```bash
python3 scripts/autoupdate_roadmap.py --next
```

Output shows:

- Current phase
- Next milestone
- Next task to execute

### Execute Next Iteration

Type in your message:

```
/autoupdate
```

The system will:

1. Read ROADMAP.md
2. Identify next incomplete task
3. Execute one iteration cycle
4. Update ROADMAP with progress
5. Report what was completed

---

## How Autoupdate Works

### The Iteration Cycle

When you type `/autoupdate`, the system executes this cycle:

```
1. PLAN PHASE (5 min)
   ├─ Analyze current task
   ├─ Break into subtasks
   └─ Identify dependencies

2. EXECUTE PHASE (20-60 min)
   ├─ Complete one subtask
   ├─ Create/modify files
   ├─ Run scripts
   └─ Generate outputs

3. VALIDATE PHASE (5-10 min)
   ├─ Test results
   ├─ Verify correctness
   └─ Check against criteria

4. DOCUMENT PHASE (5 min)
   ├─ Record what was done
   ├─ Update ROADMAP
   └─ Save progress

5. REVIEW PHASE (5 min)
   ├─ Check against success criteria
   ├─ Identify blockers
   └─ Plan next iteration

6. ITERATE
   └─ Move to next subtask or task
```

### Task Status Indicators

In the ROADMAP, tasks are marked with:

- `[ ]` - Not started
- `[~]` - In progress
- `[x]` - Completed
- `[!]` - Blocked/Issue
- `[?]` - Needs clarification

### Sequential Processing

Tasks are executed **one at a time**, not in parallel:

```
Iteration 1: M1.1 Task 1 ✓
Iteration 2: M1.1 Task 2 ✓
Iteration 3: M1.1 Task 3 ✓
Iteration 4: M1.2 Task 1 ✓
Iteration 5: M1.2 Task 2 ✓
...
```

---

## Current Roadmap Structure

### Phase 1: Core Enhancement (Weeks 1-4)

**Status:** Ready to start  
**Effort:** 40-60 hours

#### M1.1: Image Generation (Week 1-2)

- Generate 165 place images
- Generate 20 guide images
- Validate and optimize
- Organize in directories

#### M1.2: Data Enrichment (Week 2-3)

- Write descriptions (43 capsules)
- Create highlights (43 capsules)
- Assign ratings
- Add practical information

#### M1.3: Website Components (Week 3-4)

- Create CapsuleGallery component
- Create HighlightsBadges component
- Create RatingStars component
- Create PracticalInfo component
- Update pages

### Phase 2: Advanced Features (Weeks 5-6)

**Status:** Coming soon

#### M2.1: Search & Filtering

- Implement full-text search
- Create advanced filter component
- Add autocomplete

#### M2.2: Recommendations Engine

- Implement "similar places" algorithm
- Create recommendation component
- Add favorites system

### Phases 3-6: Future Phases

- Phase 3: Performance & Optimization
- Phase 4: Testing & Quality Assurance
- Phase 5: Deployment & Launch
- Phase 6: Post-Launch Enhancements

---

## Using the Autoupdate System

### Basic Usage

**Step 1: Check Status**

```bash
python3 scripts/autoupdate_roadmap.py --status
```

**Step 2: View Next Task**

```bash
python3 scripts/autoupdate_roadmap.py --next
```

**Step 3: Execute Iteration**
Type in your message:

```
/autoupdate
```

**Step 4: Repeat**
After each iteration, the ROADMAP is updated and you can trigger the next iteration.

### Continuous Execution

To execute multiple iterations in sequence:

```
/autoupdate
(System completes iteration 1)

/autoupdate
(System completes iteration 2)

/autoupdate
(System completes iteration 3)

...and so on
```

### Checking Progress

After each `/autoupdate` command, the system will:

1. Show what was completed
2. Update ROADMAP.md with new status
3. Suggest next task
4. Provide metrics and statistics

---

## Task Breakdown Strategy

### How Tasks Are Broken Down

Each major task (milestone) is broken into:

1. **Subtasks** - Smaller, manageable units (1-3 hours each)
2. **Checkpoints** - Validation points after each subtask
3. **Deliverables** - Concrete outputs
4. **Effort Estimates** - Time requirements
5. **Success Criteria** - Measurable outcomes

### Example: M1.1 Image Generation

**Main Task:** Generate 185 images

**Subtasks:**

1. Generate 165 place images (5 per place)
2. Generate 20 guide images (2 per guide)
3. Validate image quality
4. Optimize for web
5. Organize in directories
6. Create inventory report

**Each Iteration:**

- Completes 1-2 subtasks
- Takes 20-60 minutes
- Produces concrete outputs
- Validates against criteria

---

## Resources & Tools

### Documentation Files

- `ROADMAP.md` - Main roadmap with all phases and tasks
- `docs/CAPSULE_ENHANCEMENT_PLAN.md` - Enhancement plan
- `docs/CAPSULE_ENHANCEMENT_README.md` - Quick start guide
- `docs/ENHANCEMENT_SYSTEM_INDEX.md` - System index
- `docs/ROADMAP_AUTOUPDATE_GUIDE.md` - This file

### Scripts

- `scripts/autoupdate_roadmap.py` - Roadmap parser and status tool
- `scripts/enrich_capsules.py` - Capsule enrichment script
- `scripts/validate_capsules.py` - Validation script

### Prompts & Templates

- `prompts/place_image_prompts.json` - 165 place image prompts
- `prompts/guide_image_prompts.json` - 20 guide image prompts
- `data/enrichment_templates/place_template.json` - Place template
- `data/enrichment_templates/guide_template.json` - Guide template

---

## Examples

### Example 1: View Current Status

```bash
$ python3 scripts/autoupdate_roadmap.py --status

================================================================================
ROADMAP STATUS
================================================================================

Phase 1: Core Enhancement
  ○ M1.1: Image Generation
     Progress: 0/6 (0%)
  ○ M1.2: Data Enrichment
     Progress: 0/8 (0%)
  ○ M1.3: Website Components
     Progress: 0/9 (0%)

Phase 2: Advanced Features
  ○ M2.1: Search & Filtering
     Progress: 0/7 (0%)
  ○ M2.2: Recommendations Engine
     Progress: 0/7 (0%)

================================================================================
```

### Example 2: View Next Task

```bash
$ python3 scripts/autoupdate_roadmap.py --next

================================================================================
NEXT TASK
================================================================================

Phase 1: Core Enhancement
Milestone: M1.1 - Image Generation
Task: Generate 165 place images (5 per place)

================================================================================
```

### Example 3: Execute Iteration

```
User: /autoupdate

System Response:
================================================================================
ITERATION 1 - PHASE 1, MILESTONE M1.1
================================================================================

Current Task: Generate 165 place images (5 per place)

PLAN PHASE:
✓ Analyzed task
✓ Breaking into subtasks:
  1. Generate place images 1-20
  2. Generate place images 21-33
  3. Validate quality
  4. Optimize for web
  5. Organize in directories

EXECUTE PHASE:
✓ Generated 20 place images
✓ Validated quality
✓ Optimized images
✓ Organized in /client/public/images/capsules/place/

VALIDATE PHASE:
✓ All 20 images present
✓ File sizes < 500 KB
✓ Format: JPG/WebP
✓ Quality: Excellent

DOCUMENT PHASE:
✓ Updated ROADMAP.md
✓ Recorded progress
✓ Saved iteration results

REVIEW PHASE:
✓ Checked against success criteria
✓ No blockers identified
✓ Ready for next iteration

================================================================================
SUMMARY
================================================================================
Completed: Generate 20 place images (1/2)
Effort: 45 minutes
Status: ✓ Success
Next: Generate remaining 145 place images

Type /autoupdate again to continue
================================================================================
```

---

## Customization

### Adjusting Effort Estimates

If you find tasks take longer/shorter than estimated:

1. Open `ROADMAP.md`
2. Find the task
3. Update the effort estimate
4. Continue with next iteration

### Modifying Tasks

To add, remove, or modify tasks:

1. Open `ROADMAP.md`
2. Edit the task list
3. Update success criteria
4. Continue with autoupdate

### Reordering Priorities

To change task priority:

1. Open `ROADMAP.md`
2. Reorder tasks/milestones
3. Update timeline if needed
4. Continue with autoupdate

---

## Troubleshooting

### "Next task not found"

**Cause:** All tasks are completed or ROADMAP is malformed  
**Solution:**

1. Check ROADMAP.md syntax
2. Verify task checkboxes are formatted correctly
3. Run `python3 scripts/autoupdate_roadmap.py --status`

### "Task blocked"

**Cause:** Task depends on incomplete prerequisites  
**Solution:**

1. Mark task with `[!]` status
2. Note blocker in ROADMAP
3. Complete prerequisite tasks first
4. Unblock task when ready

### "Progress not updating"

**Cause:** ROADMAP.md not being saved correctly  
**Solution:**

1. Verify file permissions
2. Check file is not locked
3. Manually update ROADMAP if needed
4. Commit changes to git

---

## Best Practices

### For Effective Autoupdate Usage

1. **Keep ROADMAP Updated**
   - Update status after each iteration
   - Record actual effort vs. estimated
   - Note any blockers or issues

2. **Use Consistent Formatting**
   - Use `[ ]`, `[x]`, `[~]`, etc. consistently
   - Keep task descriptions clear and concise
   - Maintain proper indentation

3. **Break Tasks Appropriately**
   - Each iteration should take 20-60 minutes
   - Not too small (< 15 min)
   - Not too large (> 2 hours)

4. **Validate After Each Iteration**
   - Test outputs
   - Check against success criteria
   - Document results

5. **Review Progress Regularly**
   - Check status weekly
   - Adjust timeline if needed
   - Celebrate milestones

---

## Timeline

| Phase | Duration | Start  | End    | Status |
| ----- | -------- | ------ | ------ | ------ |
| 1     | 4 weeks  | Dec 2  | Dec 30 | Ready  |
| 2     | 2 weeks  | Dec 30 | Jan 13 | Coming |
| 3     | 1 week   | Jan 13 | Jan 20 | Coming |
| 4     | 1 week   | Jan 20 | Jan 27 | Coming |
| 5     | 1 week   | Jan 27 | Feb 3  | Coming |
| 6     | Ongoing  | Feb 3  | TBD    | Coming |

**Total:** 9-10 weeks, 150-200 hours

---

## Next Steps

1. **Review ROADMAP.md**
   - Read the full roadmap
   - Understand all phases
   - Check current status

2. **Start First Iteration**
   - Type `/autoupdate`
   - System executes M1.1 iteration 1
   - Review results

3. **Continue Iterations**
   - Type `/autoupdate` after each iteration
   - System progresses through tasks
   - ROADMAP updates automatically

4. **Monitor Progress**
   - Check status regularly
   - Adjust timeline as needed
   - Celebrate milestones

---

## Support

For questions or issues:

1. Check this guide
2. Review ROADMAP.md
3. Check script documentation
4. Review task descriptions
5. Type `/autoupdate help`

---

**Last Updated:** December 2, 2025  
**Status:** Ready for Use  
**Next Step:** Type `/autoupdate` to begin Phase 1
