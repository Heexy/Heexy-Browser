import os
import re
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Input
# from textual import events
# from textual.reactive import reactive
import colorama
from colorama import Fore, Style
from rich.text import Text
from textual.widgets import RichLog
import asyncio
import yaml
import shutil
from distutils.dir_util import copy_tree

# import nest_asyncio
# nest_asyncio.apply()


# Initialize Colorama for handling colored output
colorama.init(autoreset=True)

startingdir = os.getcwd()

build_dir = f"{startingdir}/obj-x86_64-pc-windows-msvc"
profile_dir = f"{startingdir}\\plinK_data\\profile"

if not os.name == 'nt':
    print(f"{Fore.RED}The plinK build tool is not available on your system")
    input(f"{Fore.RESET} Press enter to exit")
    quit(1)

try:
    os.makedirs("plinK_data")
except:
    pass


# class LogWidget(Static):
#     """A widget to display log messages with automatic scrolling."""
#
#     content = reactive("")
#     _scroll_top = reactive(0.0)
#
#     def update_log(self, message: str):
#         """Append a message to the log content and scroll to the bottom."""
#         self.content += message + "\n"
#         self.update(self.content)
#         self.scroll_to_bottom()
#
#     def scroll_to_bottom(self):
#         """Scroll to the bottom of the log widget."""
#         # Force an update to ensure the scroll position is recalculated
#         self._scroll_top = 1.0  # Set vertical scroll position to the bottom
#
#     def render(self) -> str:
#         """Render the content of the widget."""
#         return self.content

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def remove_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class LogHandler:
    """Handles logging messages with different severity levels."""

    def __init__(self, log_widget):
        self.start_time = datetime.now()
        self.log_widget = log_widget

    def log(self, message, level="i"):
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Define log levels and corresponding Colorama colors
        levels = {
            "i": ("INFO", Fore.CYAN),
            "w": ("WARNING", Fore.YELLOW),
            "e": ("ERROR", Fore.RED),
            "d": ("DEBUG", Fore.GREEN)
        }

        # Get the level name and color
        level_name, color = levels.get(level, ("INFO", Fore.WHITE))
        lines = str(message).split("\\n")
        # self.log_widget.write(lines)
        for line in lines:
            line = remove_ansi_codes(line)
            # Format the log message with Colorama color codes
            log_message = f"— [{timestamp}] [{level_name}] {color}{line}{Fore.RESET} —"
            log_message = Text.from_ansi(log_message)

            # Add the log message to the widget (without ANSI codes)
            self.log_widget.write(log_message)


class StartApp(App):
    """A Textual App to display two windows, log messages, and accept user input."""

    CSS = """
    Screen {
        layout: vertical;
    }
    .window {
        border: wide;
        padding: 1;
    }
    #top {
        height: 1fr;
    }
    #bottom {
        height: 1fr;
        overflow-y: auto;
    }
    #input {
        height: 3;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.PRESERVE_FOLDER = None
        self.log_handler_top = None
        self.log_handler = None
        self.input_active = False
        self.user_input_event = asyncio.Event()
        self.user_input_value = None
        self.task_finished_event = asyncio.Event()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            RichLog(classes="window", id="top"),
            RichLog(classes="window", id="bottom", auto_scroll=True)
        )
        yield Input(placeholder="Enter command for plinK", id="input", disabled=True)
        yield Footer()

    async def _read_stream(self, stream, cb):
        """Asynchronously read the output of a stream line by line in real time."""
        while True:
            line = await stream.readline()
            if line:
                cb(line)  # Log each line immediately as it is read
            else:
                break

    async def _run_subprocess(self, cmd, stdout_cb, stderr_cb, cwd):
        """Runs a subprocess with real-time logging of stdout and stderr."""
        # Set environment variables to disable output buffering in the Python subprocess
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        # Start the subprocess with unbuffered output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env  # Pass the unbuffered environment to the process
        )

        # Capture output from stdout and stderr asynchronously in real time
        await asyncio.gather(
            self._read_stream(process.stdout, stdout_cb),
            self._read_stream(process.stderr, stderr_cb)
        )

        # Wait for the subprocess to finish
        task_complete_signal = await process.wait()
        return task_complete_signal

    async def run_mach(self, command):
        """Handles running mach through Python and logging output in real time."""
        self.log_handler.log(f"Running command: {command}", "i")
        cmd = ["python", f"{startingdir}/mach"] + command.split()

        # Real-time stdout and stderr logging
        asyncio.create_task(
            self._run_subprocess(
                cmd,
                lambda x: self.log_handler_top.log(x.decode().strip(), "i"),  # Real-time logging of stdout
                lambda x: self.log_handler_top.log(x.decode().strip(), "e"),  # Real-time logging of stderr
                cwd=startingdir
            )
        )

    async def run_cmd(self, command):
        self.log_handler.log(f"Running command: {command}", "i")
        cmd = command.split()

        # Real-time stdout and stderr logging
        asyncio.create_task(
            self._run_subprocess(
                cmd,
                lambda x: self.log_handler_top.log(x.decode().strip(), "i"),  # Real-time logging of stdout
                lambda x: self.log_handler_top.log(x.decode().strip(), "e"),  # Real-time logging of stderr
                cwd=startingdir
            )
        )

    async def on_mount(self):
        """Called when the app is ready to start."""
        # Initialize the log handler with the bottom window (log widget)
        self.bottom_window = self.query_one("#bottom", RichLog)
        self.top_window = self.query_one("#top", RichLog)
        self.log_handler = LogHandler(self.bottom_window)
        self.log_handler_top = LogHandler(self.top_window)

        # Log some messages
        self.log_handler.log("plinK", "i")
        self.log_handler.log("Setting up windows", "i")
        await asyncio.sleep(1)  # TODO: Find a better way to get when the window is created/loaded

        # Check if it's the first start
        if not os.path.exists(f"{startingdir}/plinK_data/first_start.plink"):
            self.log_handler.log("First run", "w")
            # self.log_handler.log("Need to clear cache", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Run ./mach bootstrap if you don't have mach set-up", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Starting build...")
            task = asyncio.create_task(self.run_mach("build"))
            await task
            # Activate input after the warning message
            # self.user_input_event.clear()
            # task = asyncio.create_task(self.activate_input())
            # await task
            self.log_handler.log("Creating build config file")
            with open(f"{startingdir}/plinK.buildconfig", "x"):
                pass
            with open(f"{startingdir}/plinK.buildconfig", "w") as f:
                f.write("""preserve_bookmarks: true
preserve_profile: true
preserve_extensions: true
preserve_folders: []""")
            await asyncio.sleep(1)
            self.log_handler.log(f"Done!")
            self.log_handler.log("--------------------------------")
            self.log_handler.log(f"plinK's buildconfig file is in {startingdir}/plinK.buildconfig", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Finishing up...")
            with open(f"{startingdir}/plinK_data/first_start.plink", "x"):
                pass
            self.log_handler.log("Some features might not work while mach is building", "w")
            self.log_handler.log("Most features will not work until you create a user profile/run your build", "w")
        self.log_handler.log("Loading config...")
        config = load_config(f"{startingdir}/plinK.buildconfig")
        self.PRESERVE_PROFILE = bool(config["preserve_profile"])
        self.PRESERVE_EXTENSIONS = bool(config["preserve_extensions"])
        self.PRESERVE_FOLDERS = config["preserve_folders"]
        self.PRESERVE_BOOKMARKS = bool(config["preserve_bookmarks"])

        #     os.chdir(startingdir)
        #     self.log_handler_top.log(self.execute(f"test.bat", lambda x: print("STDOUT: %s" % x),
        # lambda x: print("STDERR: %s" % x), cwd=startingdir))
        # self.log_handler_top.log(os.system("test.bat"))
        task = asyncio.create_task(self.activate_input())
        await task
        self.log_handler.log("Waiting for command...", "i")
        # await self.run_mach("build")

    # async def run_process(self, command):
    #     self.log_handler_top.log(command)
    #     process = await asyncio.create_subprocess_exec(
    #         *command.split(),
    #         shell=True,# Replace with your command
    #         # stdout=asyncio.subprocess.PIPE,
    #         # stderr=asyncio.subprocess.PIPE,
    #         # bufsize=0
    #     )
    #     # stdout, _ = yield process.communicate()
    #
    #     self.log_handler_top.log("created process")
    #     while True:
    #         try:
    #             output = await asyncio.wait_for(process.stdout.readline(),
    #                                             timeout=5.0)  # Increased timeout to 5 seconds
    #             if output:
    #                 self.call_from_thread(self.log_output, output.decode().strip())
    #             else:
    #                 break
    #         except asyncio.TimeoutError:
    #             self.log_handler_top.log("timeout")
    #             if process.poll() is not None:
    #                 break
    #             continue
    #
    #     # Check the exit code of the process
    #     exit_code = await process.wait()
    #     self.log_handler_top.log(f"Process exited with code {exit_code}")
    #
    # def log_output(self, output: str) -> None:
    #     if output:  # Check if output is not empty
    #         self.log_handler_top.log(output)

    async def get_user_input(self):
        await self.user_input_event.wait()

        return self.user_input_value

    async def activate_input(self):
        """Activate the input field."""
        self.input_active = True
        input_box = self.query_one(Input)
        input_box.disabled = False  # Enable the input field
        input_box.focus()  # Set focus to the input field
        await asyncio.sleep(0)

    async def deactivate_input(self):
        """Deactivate the input field after user input."""
        self.input_active = False
        input_box = self.query_one(Input)
        input_box.disabled = True  # Disable the input field
        await asyncio.sleep(0)

    async def profile_build(self):
        try:
            shutil.rmtree(f"{profile_dir}/cache2")
        except:
            pass
        self.log_handler.log("Building profile...")
        self.log_handler_top.log("Mach output may interfere with profile building")
        if self.PRESERVE_PROFILE:
            self.log_handler.log("Copying profile")
            copy_tree(f"{build_dir}/tmp/profile-default", f"{profile_dir}")
            shutil.rmtree(f"{profile_dir}/cache2")
            self.log_handler.log("Done")
            return asyncio.sleep(0)
        if self.PRESERVE_EXTENSIONS:
            self.log_handler.log("Preserving extensions")
            try:
                os.makedirs(f"{startingdir}/plinK_data/profile")
            except:
                pass
            copy_tree(f"{build_dir}/tmp/profile-default/extension-store", f"{profile_dir}/extension-store")
            self.log_handler.log("1/8")
            copy_tree(f"{build_dir}/tmp/profile-default/extension-store-menus", f"{profile_dir}/extension-store-menus")
            self.log_handler.log("2/8")
            copy_tree(f"{build_dir}/tmp/profile-default/browser-extension-data",
                      f"{profile_dir}/browser-extension-data")
            self.log_handler.log("3/8")
            copy_tree(f"{build_dir}/tmp/profile-default/extension-store", f"{profile_dir}/extension-store")
            self.log_handler.log("4/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/addons.json", f"{profile_dir}/addons.json")
            self.log_handler.log("5/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/addonStartup.json.lz4",
                            f"{profile_dir}/addonStartup.json.lz4")
            self.log_handler.log("6/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/extension-preferences.json",
                            f"{profile_dir}/extension-preferences.json")
            self.log_handler.log("7/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/extensions.json", f"{profile_dir}/extensions.json")
            self.log_handler.log("8/8")
            self.log_handler.log("Done")
        if self.PRESERVE_BOOKMARKS:
            self.log_handler.log("Preserving bookmarks")
            copy_tree(f"{build_dir}/tmp/profile-default/bookmarkbackups", f"{profile_dir}/bookmarkbackups")
            self.log_handler.log("Done")
        if self.PRESERVE_FOLDER:
            self.log_handler.log("Preserving folders")
            for dir in self.PRESERVE_FOLDERS:
                copy_tree(dir, f"{profile_dir}")
            self.log_handler.log("Done")
        shutil.rmtree(f"{profile_dir}/cache2")
        self.log_handler.log("Profile building done!")
        return asyncio.sleep(0)

    async def on_input_submitted(self, event: Input.Submitted):
        """Handle user input when they press Enter."""
        if self.input_active:
            user_input = event.value
            # self.log_handler.log(f"User input: {user_input}", "i")
            self.user_input_value = user_input
            await self.deactivate_input()
            self.user_input_event.set()  # Notify that input has been received
            if user_input == "profile build":
                task = asyncio.create_task(self.profile_build())
                await task
            elif user_input == "profile push":
                self.log_handler.log("Pushing profile into rundir...")
                copy_tree(profile_dir, f"{build_dir}/tmp/profile-default")
                self.log_handler.log("Done")
            elif user_input == "profile sync prefs":
                shutil.copy(f"{build_dir}/tmp/profile-default/prefs.js", profile_dir)
                shutil.copy(f"{build_dir}/tmp/profile-default/user.js", profile_dir)
            elif user_input.startswith("build"):
                self.log_handler.log(f"app_build", "d")
                self.log_handler.log(f"Building...")
                task = asyncio.create_task(self.run_mach("build"))
                await task
            elif user_input == "run":
                self.log_handler.log(f"Copying profile...")
                self.log_handler.log(f"Profile in {build_dir}/tmp/profile-default WILL BE LOST", "w")
                copy_tree(profile_dir, f"{build_dir}/tmp/profile-default")
                await asyncio.sleep(1)
                # task = asyncio.create_task(self.run_cmd(f"{build_dir}/dist/bin/firefox.exe -profile '{build_dir}/tmp/profile-default'"))
                task = asyncio.create_task(self.run_mach("run"))
                await task
            elif user_input.startswith("logs"):
                await self.deactivate_input()
                await asyncio.sleep(2)
            elif user_input == "clear cache":
                task = asyncio.create_task(self.run_mach("clobber"))
                await task
            elif user_input == "rd":
                self.log_handler.log("Redrawing...", "w")
                self.bottom_window.refresh()
                self.log_handler.log("Bottom window redrawn")
                self.top_window.refresh()
                self.log_handler_top.log("Top window redrawn")
                await self.deactivate_input()
                input_box = self.query_one(Input)
                input_box.refresh()
                await self.activate_input()
                self.log_handler.log("Input redrawn")
            elif user_input.startswith("mach"):
                cmd_by_usr_input = user_input.split(" ")[:1]
                task = self.run_mach("".join(cmd_by_usr_input))
                await task
            elif user_input == "close" or user_input == "quit":
                return 0
            else:
                self.log_handler.log("Unknown command", "e")

            await asyncio.sleep(0)
            await self.activate_input()
            return user_input

    async def wait_for_input(self):
        """Wait until the user has submitted input."""
        # Clear the event before waiting
        await self.user_input_event.wait()  # Wait for the event to be set
        return self.user_input_value


# Run the app
if __name__ == "__main__":
    StartApp().run()
