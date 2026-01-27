# Setting up Mac

Based off of Jon Halverson's: https://github.com/jdh4/mac_productivity/tree/main/raycast

## Karabiner-Elements + Raycast
- Karabiner-Elements: https://karabiner-elements.pqrs.org/
- Karabiner-EventViewer: Shows what keys are being pressed (useful for creating rules)
- Raycast: https://www.raycast.com/
  - Uses Karabiner-Elements under the hood
  - raycast > Export Settings & Data > copy file to another computer > Import Settings & Data

## Installation
1. karabiner-elements setup:
   1. `cp karabiner_config/karabiner.json ~/.config/karabiner/karabiner.json`
   2. **Remaps caps lock to command+control+option+shift**.
2. macos > system settings > keyboard > keyboard shortcuts > spotlight > disable spotlight search
3. raycast > `cmd + ,` > general > raycast hotkey > `cmd + space`
4. raycast > extensions > search files > add alias > `caps + f`
   1. raycast > extensions > search files > Search By > Change "Name" to "Name and Contents"
5. raycast > extensions > clipboard > clipboard history > add alias > `caps + v`
6. raycast adding scripts: raycast > extensions > scripts > Add Directory > Point it to this project's `raycast_scripts` directory
7. raycast > extensions > quicklinks > Pass selected text as argument (turn on)
   1. raycast > extensions > quicklinks > search google > `caps + g`

## Development
- raycast tracks user-specified directories (for scripts). No syncing needed as we work directly with the source.
- karabiner-elements uses json file which we can sync the local version (for vcs) and the one used on the machine.
  - use `sync_karabiner.sh` to sync the local version to the machine.


## Agent Usage
 
Sync .claude directory, mapping the directory tree, into a target directory's .claude directory. symlinks all leaf files.

```bash
./sync_claude.py <target_folder> --clean-old-symlinks
```

## Things to think about:
- Dynamic placeholders (like {cursor} and {date}) can be used with raycast snippets and quicklinks
- [raycast snippets](https://manual.raycast.com/snippets): store and insert frequently used text with dynamic placeholders
- [raycast quicklinks](https://manual.raycast.com/quicklinks): 
  - if website provides search through url, i.e. google translate, can add as quicklink

## FAQ
Q: My external keyboard is not recognizing karabiner-elements rules (remappings)
A: Configurations > Devices > Modify events (set on) > Treat as built-in keyboard (set on)