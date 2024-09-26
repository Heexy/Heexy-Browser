
---

# 🐱 plinK - Firefox Build Tool Extension
By Heexy

## Table of Contents
1. [Getting Things Set Up](#1-getting-things-set-up)
2. [Modifying Your Browser Profile](#2-modifying-your-browser-profile)
3. [Building Firefox](#3-building-firefox)
4. [Building the Profile](#4-building-the-profile)
5. [Running Firefox](#5-running-firefox)
6. [Other Commands](#6-other-commands)
7. [Known issues](#7-known-issues)

---

## 1. Getting Things Set Up

### 💪 Requirements:
- **plinK** currently only supports **Windows** (NT-based systems).
- A terminal with a modern rendering engine, that supports dynamic redraw. (Most IDE terminals won't work. Terminals with AtlasEngine might sometimes see blue text as pink)
- Ensure that the Firefox source code and the **mach** build tool are available in your working directory.
- Ensure, that you have python and the proper packages installed (automatic package installer coming soon)

### 🚀 First Run Instructions:
1. Clone the Heexy browser source code to your system. (Ideally onto a dev drive.)
2. Run `./mach bootstrap` and select the second option
3. After it finishes open a terminal of your choice in the newly cloned Heexy browser source directory and run `python plink.py`
4. `plinK` will automatically setup it's build environment
   - It will create a `plinK.buildconfig` file where you can configure profile and extension preservation options.
   - It will also build Heexy browser for the first time - First build can take more than an hour to complete
5. After it finishes building the first build it's recommended to run the `run` command using the plonKsole (plinK's console). This will create the default user profile.
6. Modify this profile to your needs [(More about that here)](#2-modifying-your-browser-profile)
7. Verify, that your changes are reproducible [(How?)](#3-building-firefox)
8. Verify, that other team members like your changes
9. Once you get the green flag from others `push` your changes to GitHub

---

## 2. Modifying Your Browser Profile

By default, plinK preserves everything in the browser profile folder (except cache)

- To modify these settings, edit the `plinK.buildconfig` file, which includes options for:
  - Preserving bookmarks.
  - Preserving profile settings.
  - Preserving extensions.
  - Preserving specific folders.
  - _(the plinK.buildconfig file is a .yaml file with a different extension)_
  
Modifying the user profile
 - The recommended way:
    - Run Heexy browser through the plonKsole
        - Modifying the bundled extensions
            - To add an extension to be bundled with the browser load it using `about:debugging` [(Most extensions won't install)](#7-known-issues) 
            - To remove an extension, simply remove the extension in the settings
        - Modifying other settings:
            - The GUI way:
                - Modify settings normally in the browser settings
                - Or using `about:config`
            - The (recommended) modifying source way:
                - Edit the .js files in `browser/app/profile`
                - Remember to run `build` in the plonKsole, otherwise your changes won't apply
---

## 3. Building Firefox

To build Heexy browser using `plinK`, run the following command in the plonKsole:

```bash
build
```

This will trigger the `mach build` process, which compiles the Heexy browser source code into an executable version. Ensure you have the necessary tools and environment set up for building Heexy browser before starting this process.
_(Note: This will not build your current profile, and it may discard your current browser profile (build_dir/tmp/profile-default) )_


---

## 4. Building the Profile

Building the profile makes a snapshot of your current profile (by default it takes a snapshot of everything except cache) and saves it, so your changes can be replicated in production.
For you, it means that you should run this command if one or more of these conditions are met:
- After modifying the profile (If you modified the profile by modifying the source code make sure to run [`profile sync prefs`](#6-other-commands) to sync the current user.js and prefs.js with the last built profile)
- Before pushing onto GitHub
- Before testing any changes, that you have made (Ignore this condition if you already built the profile after making the changes)
- When you want to save the active profile

You can build your Heexy browser profile with preserved data using the following command in the plonKsole:

```bash
profile build
```

### ✨ Profile Data Preservation:
- Bookmarks, extensions, and specific folders can be copied over from the `obj-x86_64-pc-windows-msvc/tmp/profile-default` directory to the `plinK_data/profile` folder.
  
- **Profile options** can be configured in `plinK.buildconfig` for:
  - Preserving bookmarks.
  - Extensions.
  - Folders you wish to save.

_(Make sure to run this before pushing to GitHub)_

---

## 5. Running Firefox

Once Heexy browser is built and the profile is configured, you can launch it using:

```bash
run
```

This command will:
- Copy built profile into the profile directory(so it's used by Heexy browser) [Profile building info here](#4-building-the-profile)
- Launch Heexy browser with your custom profile.
  
---

## 6. Other Commands

### ♻️ Clearing the Cache:
To clear Firefox’s build cache, use the command:

```bash
clear cache
```

### 📣 Pushing Profile to Run Directory:
You can manually push the profile into the Firefox run directory using:

```bash
profile push
```

### 🎨 Redrawing UI:
If you encounter any issues with the UI, you can refresh it with:

```bash
rd
```
([Mach may sometimes brick the UI](#7-known-issues) for the entire length of a build, it is recommended to run this command after mach finished building (Make sure to delete the build command from the input before inputting this command))

### 📜 Viewing Logs:
Some terminal renderers block scrolling when the user input widget is focused.
To unfocus the user input widget use:

```bash
logs
```

### 🔄 Syncing prefs.js and user.js:
To sync config files with a built profile you can use this command in the plonKsole:
```bash
profile sync pref
```

### ❌ Closing plinK:
To close plinK run this command in the plonKsole:
```bash
close
```
and then press `ctrl+c` to close plinK
(You can also use the `quit` command)
(Using only ctrl+c is not recommended as you may interrupt some operations)

---
## 7. Known Issues
- Extensions need to be installed through `about:debugging`. **If the extension does more than just modifying settings IT WILL ONLY BE INSTALLED TEMPORARILY**. That means, that most extensions won't be able to install. (This is not a problem with plinK)
- Long Mach builds breaking rendering (invalid ascii color codes) on certain terminals
---

## 👀 License
PlinK is licensed as [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

## 📌 Note
This documentation outlines the key commands and processes for using plinK. For any additional help, refer to the in-app log messages or contact Heexy devs.

---
