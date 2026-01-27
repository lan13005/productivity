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
                st = os.lstat(src)  # don't follow symlinks
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


def main():
    parser = argparse.ArgumentParser(
        description="Mirror the directory tree of src_claude into tgt_dir by symlinking leaf files."
    )
    parser.add_argument(
        "--tgt_dir",
        default="../analyze-jds",
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
    args = parser.parse_args()

    src_root = os.path.abspath(os.path.expanduser(args.src))
    tgt_root = os.path.abspath(os.path.expanduser(args.tgt_dir))
    
    if os.path.basename(tgt_root) != '.claude':
        tgt_root = find_claude_directories(tgt_root, depth=args.depth)
        if len(tgt_root) != 1:
            raise SystemExit(f"ERROR: Multiple .claude directories found at depth {args.depth}: {tgt_root}")
        tgt_root = tgt_root[0]
        print(f"\nWARNING! You did not specify a .claude directory but we found the following: {tgt_root}\n")

    if not os.path.isdir(src_root):
        raise SystemExit(f"ERROR: src_claude does not exist or is not a directory: {src_root}")

    os.makedirs(tgt_root, exist_ok=True)

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
