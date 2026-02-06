#!/usr/bin/env python3
"""Sync .claude directory, mapping the directory tree, into a target directory's .claude
directory. symlinks all leaf files.
"""

import os
import argparse

def find_claude_directories(root_dir: str, depth: int = 1):
    """Search for .claude directories within root_dir up to `depth` levels deep."""
    root_dir = os.path.abspath(os.path.expanduser(root_dir))
    found = []

    if depth < 0:
        return found

    for current_root, dirs, _files in os.walk(root_dir):
        rel = os.path.relpath(current_root, root_dir)
        current_depth = 0 if rel == "." else len(rel.split(os.sep))

        # Stop descending if we're deeper than allowed
        if current_depth > depth:
            dirs[:] = []
            continue

        if ".claude" in dirs:
            claude_path = os.path.join(current_root, ".claude")
            found.append(os.path.abspath(claude_path))
            # Avoid finding nested .claude under this one
            dirs.remove(".claude")

    return found

def iter_file_endpoints(root: str):
    """
    Yield (src_abs_path, rel_path_from_root) for all 'dangling endpoints' in the
    directory tree: files and symlinks that are not directories.
    """
    root = os.path.abspath(os.path.expanduser(root))

    for cur_root, dirs, files in os.walk(root, followlinks=False):
        # Exclude hidden dirs? (Not requested; keep everything)
        for name in files:
            src = os.path.join(cur_root, name)
            try:
                os.lstat(src)  # don't follow symlinks
            except OSError:
                continue

            # Skip if it's somehow a dir entry (rare via weird FS); otherwise treat as endpoint
            if os.path.isdir(src) and not os.path.islink(src):
                continue

            rel = os.path.relpath(src, root)
            yield os.path.abspath(src), rel

        # Note: directories are handled implicitly by rel parent creation


def ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def clean_old_symlinks(claude_dir: str):
    """
    Remove all symlinks in all subdirectories of the .claude directory.
    
    Args:
        claude_dir: Path to the .claude directory to clean
    """
    claude_dir = os.path.abspath(os.path.expanduser(claude_dir))
    
    if not os.path.isdir(claude_dir):
        raise SystemExit(f"ERROR: .claude directory does not exist: {claude_dir}")
    
    removed = 0
    
    for root, dirs, files in os.walk(claude_dir):
        for name in files + dirs:
            path = os.path.join(root, name)
            if os.path.islink(path):
                try:
                    os.unlink(path)
                    print(f"[✓] Removed symlink: {path}")
                    removed += 1
                except OSError as e:
                    print(f"[!] Failed to remove symlink {path}: {e}")
    
    print(f"\nCleaned {removed} symlink(s) from {claude_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Mirror the directory tree of src_claude into tgt_dir by symlinking leaf files."
    )
    parser.add_argument(
        "tgt_dir",
        help="Target root directory to receive the mirrored tree of symlinks",
    )
    parser.add_argument(
        "--src",
        default=".claude",
        help="Source .claude directory (default: ./.claude)",
    )
    parser.add_argument(
        "--depth",
        default=1,
        help="Depth to search for .claude directories (default: 1)",
    )
    parser.add_argument(
        "--clean-old-symlinks",
        action="store_true",
        help="Clean all symlinks in all subdirectories of the .claude directory",
    )
    args = parser.parse_args()

    src_root = os.path.abspath(os.path.expanduser(args.src))
    tgt_root = os.path.abspath(os.path.expanduser(args.tgt_dir))
    
    if os.path.basename(tgt_root) != '.claude':
        found = find_claude_directories(tgt_root, depth=args.depth)
        if len(found) > 1:
            raise SystemExit(f"ERROR: Multiple .claude directories found at depth {args.depth}: {found}")
        if len(found) == 1:
            tgt_root = found[0]
            print(f"\nWARNING! You did not specify a .claude directory but we found the following: {tgt_root}\n")
        else:
            tgt_root = os.path.join(tgt_root, '.claude')

    if not os.path.isdir(src_root):
        raise SystemExit(f"ERROR: src_claude does not exist or is not a directory: {src_root}")

    os.makedirs(tgt_root, exist_ok=True)

    if args.clean_old_symlinks:
        clean_old_symlinks(tgt_root)

    linked = 0
    skipped = 0

    for src_abs, rel_path in iter_file_endpoints(src_root):
        tgt_abs = os.path.join(tgt_root, rel_path)

        if os.path.lexists(tgt_abs):
            
            print(f"\n[x] Exists, skipping: {tgt_abs}")
            skipped += 1
            continue

        ensure_parent_dir(tgt_abs)

        # Create symlink pointing to the source absolute path
        os.symlink(src_abs, tgt_abs)
        print(f"\n[✓] Linked: {src_abs} ->\n            {tgt_abs}")
        linked += 1

    print(f"\nDone. Linked: {linked}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
