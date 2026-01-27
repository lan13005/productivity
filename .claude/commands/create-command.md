# Create-Command Command

Create or update command files that document workflows and best practices based on problem/solution analysis.

## Goal

Create structured command files (`.md` files in `.claude/commands/`) that capture workflows, document problem/solution pairs from context, and establish practices to avoid recurring issues. When invoked on a markdown file, convert it to the standard command format.

## Context

Commands are markdown files that define reusable workflows for Claude to follow. This command helps create these files by:
- Analyzing surrounding context (conversation history, code, documentation) to identify problems and their solutions
- Documenting best practices to prevent similar problems
- Converting existing markdown documentation into the standardized command format
- Ensuring all commands follow a consistent structure for clarity and reusability

## Scope

This command handles:
- Creating new command files by analyzing context for problem/solution patterns
- Converting existing markdown files to command format when referenced
- Documenting practices and patterns to avoid recurring problems
- Ensuring commands follow the standard structure (Goal, Context, Scope, Constraints, Instructions, Output)

## Constraints

- Commands must be saved in `.claude/commands/` directory
- File names should be lowercase with hyphens (e.g., `create-command.md`)
- Commands must follow the standard section structure
- When updating existing files, preserve valuable content while restructuring
- When analyzing context, focus on actionable problem/solution pairs and preventive practices

## Instructions

### Default Behavior: Creating Commands from Context

When invoked without a file reference (e.g., `/create-command` or "create a command for X"):

1. **Analyze Surrounding Context**
   - Review conversation history, open files, and recent edits
   - Identify problems that were encountered or solved
   - Extract solution patterns and approaches that worked
   - Note any mistakes or issues that could have been avoided

2. **Identify Problem/Solution Pairs**
   - For each problem identified, document:
     - What the problem was
     - How it was solved
     - Why the solution worked
     - What could have prevented it

3. **Document Best Practices**
   - Extract practices, patterns, or approaches that prevent problems
   - Document workflows that lead to successful outcomes
   - Note common pitfalls and how to avoid them
   - Include validation steps or checks that catch issues early

4. **Create Command Structure**
   
   Create a markdown file at `.claude/commands/<command-name>.md` with the following sections:

   ```markdown
   # <Command Name> Command
   
   <Brief one-line description of what the command does>
   
   ## Goal
   <Clear statement of what this command aims to achieve>
   
   ## Context
   <Background information, why this command exists, when to use it>
   
   ## Scope
   <What this command covers and what it doesn't>
   
   ## Constraints
   <Limitations, requirements, prerequisites, or assumptions>
   
   ## Instructions
   <Step-by-step workflow that Claude should follow>
   
   ## Output
   <What the command produces or returns>
   ```

5. **Fill Each Section**
   - **Goal**: One clear sentence about the objective, derived from the problems solved
   - **Context**: Background explaining why this command exists, when to use it, and what problems it addresses
   - **Scope**: Boundaries of what the command handles, based on the solutions documented
   - **Constraints**: Prerequisites, limitations, and assumptions identified from context
   - **Instructions**: Step-by-step workflow incorporating best practices and avoiding documented pitfalls
   - **Output**: Expected results, files created, or messages shown

6. **Add Problem Prevention Sections** (as needed):
   - **Common Pitfalls**: List problems that were encountered and how to avoid them
   - **Best Practices**: Document practices that prevent issues
   - **Validation Steps**: Include checks that catch problems early
   - **Error Handling**: How to handle common errors based on past experience

7. **Save the File**
   - Write the complete command file to `.claude/commands/<command-name>.md`
   - Verify the file was created successfully by reading it back

### When Invoked on a Markdown File

When invoked with a file reference (e.g., `/create-command @some-file.md` or "create command from @some-file.md"):

**DO NOT ENTER PLAN MODE. PERFORM THE UPDATE IMMEDIATELY.**

1. **Read the Target File NOW**
   - Use the `Read` tool to read the referenced markdown file completely
   - Understand its current structure, content, and purpose

2. **IMMEDIATELY Transform to Command Format**
   - **Use the `Write` or `Edit` tool RIGHT NOW** to update the file
   - Do NOT write a plan. Do NOT describe what you will do. **Just transform the file.**
   - Restructure the content to follow the standard command format:
     - Extract or create a clear **Goal** section
     - Organize background into **Context** section
     - Define boundaries in **Scope** section
     - Document limitations in **Constraints** section
     - Convert procedures into structured **Instructions** section
     - Specify expected **Output** section
   - Preserve all valuable content from the original file
   - Reorganize and reformat as needed to fit the structure
   - If the file is not in `.claude/commands/`, ask if it should be moved there or create a new file there

3. **Enhance with Problem/Solution Documentation**
   - If the original file mentioned problems or issues, extract them into a "Common Pitfalls" or "Problem Prevention" section
   - Document solutions that were applied
   - Add best practices based on the content

4. **Verify Structure**
   - Ensure all standard sections are present (Goal, Context, Scope, Constraints, Instructions, Output)
   - Check that formatting is consistent
   - Verify all original valuable content is preserved

5. **Inform User**
   - Confirm the file has been updated to command format
   - Note any sections that were added or reorganized

## Output

After execution, the command should:

1. **For Context-Based Creation**:
   - A new `.md` file in `.claude/commands/` directory
   - Command structured with problem/solution pairs documented
   - Best practices and preventive measures included
   - Confirmation message showing the file path

2. **For File Conversion**:
   - Updated markdown file restructured to command format
   - All original content preserved and reorganized
   - Standard sections (Goal, Context, Scope, Constraints, Instructions, Output) present
   - Summary of transformations made

## Examples

### Example 1: Creating from Context

**User**: "Create a command for handling SLURM job analysis based on what we just did"

**Process**:
1. Analyze conversation history and recent code changes
2. Identify problems encountered (e.g., "forgot to check data format", "didn't validate inputs")
3. Extract solutions (e.g., "added validation step", "checked file format first")
4. Document practices (e.g., "always validate input format before processing")
5. Create `.claude/commands/analyze-slurm-jobs.md` with:
   - Goal: Analyze SLURM job data with proper validation
   - Context: When to use, problems it solves
   - Scope: What analysis is included
   - Constraints: Required data format, dependencies
   - Instructions: Step-by-step workflow including validation steps
   - Common Pitfalls: Problems encountered and how to avoid them
   - Output: Reports and visualizations

### Example 2: Converting a Markdown File

**User**: `/create-command @deployment-guide.md`

**What Claude Does** (immediate actions, no planning):
1. **Uses `Read` tool** to read `deployment-guide.md` completely
2. **Uses `Write` or `Edit` tool RIGHT NOW** to restructure the file:
   - Extract goal from introduction → **Goal** section
   - Move background info → **Context** section
   - Define what's covered → **Scope** section
   - List prerequisites → **Constraints** section
   - Convert steps → **Instructions** section
   - Document results → **Output** section
3. **Preserves all original content** while reorganizing
4. **Informs user** that the file has been converted to command format

### Example 3: Documenting Problem Prevention

**User**: "Create a command for the plotting workflow, including the issues we ran into"

**Process**:
1. Review recent plotting-related conversation and code
2. Identify problems:
   - Problem: "Plot labels were cut off"
   - Solution: "Added figure size adjustment and tight_layout()"
   - Prevention: "Always check figure size before saving"
3. Create command with:
   - Standard sections
   - **Common Pitfalls** section documenting the label issue and fix
   - **Best Practices** section: "Always use tight_layout() and verify figure dimensions"
   - Instructions include validation step: "Preview plot before saving"

## Security and Safety

**Never**:
- Overwrite files without user confirmation (unless explicitly updating a referenced file)
- Create commands that execute destructive operations without warnings
- Include sensitive information (API keys, passwords) in command files
- Lose original content when converting files

**Always**:
- Verify file paths before writing
- Preserve valuable content when restructuring
- Add safety warnings for dangerous operations
- Document prerequisites and constraints clearly
- Ask before moving files to `.claude/commands/` if they're elsewhere

## Error Handling

If errors occur:

- **File already exists**: Ask user if they want to update or use a different name
- **Invalid command name**: Suggest a valid name (lowercase, hyphens)
- **Missing information**: Analyze context more deeply or ask user for clarification
- **Write permission denied**: Inform user and suggest checking directory permissions
- **Malformed structure**: Fix the structure and inform user of corrections
- **Cannot read referenced file**: Inform user the file doesn't exist or cannot be accessed

## References

- Command directory: `.claude/commands/`
- Example command: `.claude/commands/commit.md`
- Project conventions: `.claude/reference/` (if exists)

## Notes

- **CRITICAL**: When converting a file, perform the transformation IMMEDIATELY. Do NOT enter plan mode. Do NOT describe what will be done. Just update the file using Write/Edit tools right away.

- When analyzing context, look for:
  - Error messages or issues mentioned
  - Solutions that were applied
  - Patterns that worked well
  - Mistakes that could have been avoided
  - Validation or checks that caught problems

- Commands should be self-contained and not require external scripts
- Use clear, actionable language in Instructions section
- Include examples for complex workflows
- Commands are meant to guide Claude's behavior, not replace it
- Always verify the command file was created/updated successfully by reading it back
- When converting files, ensure the original valuable content is preserved and reorganized, not discarded
