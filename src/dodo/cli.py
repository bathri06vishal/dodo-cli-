from __future__ import annotations

import sys
import getpass
from pathlib import Path
from typing import Optional

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import typer
import click
from click.core import Context
import questionary

from dodo.exporter import export_dataset
from dodo.filter import remove_duplicate_frames, remove_duplicate_messages
from dodo.importers import import_log
from dodo.metadata import generate_metadata
from dodo.project import create_project, find_project_root, load_config
from dodo.security import security_manager
from dodo.validation import validate_dataset


def _print_welcome() -> None:
    """Display a beautiful welcome banner with animated ASCII art."""
    import time
    import sys
    
    # ANSI color codes
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    WHITE = "\033[97m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Animated DODO banner - frame by frame
    dodo_frames = [
        f"""{BOLD}{RED}
  ██████   
  ██   ██ 
  ██   ██ 
  ██   ██ 
  ██████  {RESET}""",
        f"""{BOLD}{YELLOW}
  ██████   ██████  
  ██   ██ ██    ██ 
  ██   ██ ██    ██ 
  ██   ██ ██    ██ 
  ██████   ██████  {RESET}""",
        f"""{BOLD}{GREEN}
  ██████   ██████  ██████   
  ██   ██ ██    ██ ██   ██ 
  ██   ██ ██    ██ ██   ██ 
  ██   ██ ██    ██ ██   ██ 
  ██████   ██████  ██████  {RESET}""",
        f"""{BOLD}{CYAN}
  ██████   ██████  ██████   ██████  
  ██   ██ ██    ██ ██   ██ ██    ██ 
  ██   ██ ██    ██ ██   ██ ██    ██ 
  ██   ██ ██    ██ ██   ██ ██    ██ 
  ██████   ██████  ██████   ██████  {RESET}""",
    ]
    
    # Welcome message header
    welcome_header = f"{BOLD}{BLUE}Welcome to DODO{RESET}"
    
    typer.echo(welcome_header)
    typer.echo()
    
    # Animate the banner
    for frame in dodo_frames:
        typer.echo(frame)
        time.sleep(0.3)
        # Clear frame by moving cursor up
        sys.stdout.write("\033[6A")
        sys.stdout.flush()
    
    # Print final banner
    typer.echo(dodo_frames[-1])
    typer.echo()
    
    # Multimodal metadata description
    metadata_desc = f"""{CYAN}🤖 Multimodal Dataset Creation{RESET}
{WHITE}DODO transforms raw robotics logs into structured, ML-ready multimodal datasets.{RESET}
{WHITE}Automatically aligns sensor data (camera, IMU, lidar, actions) into synchronized frames.{RESET}
{WHITE}Generate comprehensive metadata for computer vision, robotics, and multimodal AI training.{RESET}
"""
    typer.echo(metadata_desc)
    typer.echo()
    
    # Quick commands box
    quick_commands = f"""{BLUE}╭─ Quick Commands ─────────────────────────────────────────────╮{RESET}
{BLUE}│{RESET} {YELLOW}init{RESET}                   Create a new DODO project          {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}list{RESET}                   List all DODO projects             {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}delete{RESET}                 Delete a DODO project               {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}register{RESET}               Create a new user account           {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}login{RESET}                  Login to DODO (required)           {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}import{RESET}                 Import robot logs (rosbag, JSON)   {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}generate-metadata{RESET}      Generate aligned frame metadata    {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}filter{RESET}                 Remove duplicate data (auth)        {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}validate{RESET}               Validate your dataset              {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}export{RESET}                 Export to structured format        {BLUE}│{RESET}
{BLUE}│{RESET} {YELLOW}logout{RESET}                 Logout from current session         {BLUE}│{RESET}
{BLUE}╰───────────────────────────────────────────────────────────────────────────────────────╯{RESET}

{GREEN}╭─ Examples ──────────────────────────────────────────────────────────────────────────────╮{RESET}
{GREEN}│{RESET} {WHITE}dodo register --username myuser{RESET}                              {GREEN}│{RESET}
{GREEN}│{RESET} {WHITE}dodo login --username myuser{RESET}                                 {GREEN}│{RESET}
{GREEN}│{RESET} {WHITE}dodo init my_dataset{RESET}                                        {GREEN}│{RESET}
{GREEN}│{RESET} {WHITE}dodo import log.bag --project my_dataset{RESET}                    {GREEN}│{RESET}
{GREEN}│{RESET} {WHITE}dodo filter frames --project my_dataset{RESET}                     {GREEN}│{RESET}
{GREEN}│{RESET} {WHITE}dodo export output/ --project my_dataset{RESET}                    {GREEN}│{RESET}
{GREEN}──────────────────────────────────────────────────────────────────────────────────────────╯{RESET}

{MAGENTA}Use 'dodo --help' for more information{RESET}
"""
    
    typer.echo(quick_commands)

if "ctx" not in typer.core.TyperArgument.make_metavar.__code__.co_varnames:

    def _compatible_arg_metavar(self: typer.core.TyperArgument, ctx: Context | None = None) -> str:
        if self.metavar is not None:
            return self.metavar
        var = (self.name or "").upper()
        if not self.required:
            var = f"[{var}]"
        type_var = self.type.get_metavar(param=self, ctx=ctx)
        if type_var:
            var += f":{type_var}"
        if self.nargs != 1:
            var += "..."
        return var

    def _compatible_opt_metavar(self: typer.core.TyperOption, ctx: Context | None = None) -> str:
        if self.metavar is not None:
            return self.metavar
        metavar = self.type.get_metavar(param=self, ctx=ctx)
        if metavar is None:
            metavar = self.type.name.upper()
        if self.nargs != 1:
            metavar += "..."
        return metavar

    typer.core.TyperArgument.make_metavar = _compatible_arg_metavar
    typer.core.TyperOption.make_metavar = _compatible_opt_metavar

if click.core.Parameter.make_metavar.__defaults__ is None:

    def _click_parameter_metavar(self: click.core.Parameter, ctx: Context | None = None) -> str:
        if self.metavar is not None:
            return self.metavar
        metavar = self.type.get_metavar(param=self, ctx=ctx)
        if metavar is None:
            metavar = self.type.name.upper()
        if self.nargs != 1:
            metavar += "..."
        return metavar

    def _click_argument_metavar(self: click.core.Argument, ctx: Context | None = None) -> str:
        if self.metavar is not None:
            return self.metavar
        var = self.type.get_metavar(param=self, ctx=ctx)
        if not var:
            var = (self.name or "").upper()
        if getattr(self, "deprecated", False):
            var += "!"
        if not self.required:
            var = f"[{var}]"
        if self.nargs != 1:
            var += "..."
        return var

    click.core.Parameter.make_metavar = _click_parameter_metavar
    click.core.Option.make_metavar = _click_parameter_metavar
    click.core.Argument.make_metavar = _click_argument_metavar

_typer_option_init = typer.core.TyperOption.__init__


def _compatible_typer_option_init(self: typer.core.TyperOption, **kwargs: object) -> None:
    param_decls = kwargs.get("param_decls")
    if param_decls is not None and type(param_decls) == list:
        if any(str(decl).startswith("-") for decl in param_decls):
            kwargs["param_decls"] = [decl for decl in param_decls if str(decl).startswith("-")]
    _typer_option_init(self, **kwargs)
    if not isinstance(kwargs.get("default"), bool):
        self.is_flag = False


typer.core.TyperOption.__init__ = _compatible_typer_option_init

app = typer.Typer(
    name="dodo",
    help="Convert raw robotics logs into structured multimodal ML-ready datasets.",
    no_args_is_help=False,
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def default_callback(ctx: typer.Context) -> None:
    """Show welcome page if no command is provided."""
    if ctx.invoked_subcommand is None:
        _print_welcome()


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the DODO dataset project."),
    task: str = typer.Option("navigation", "--task", "-t", help="Dataset task label.", is_flag=False),
) -> None:
    try:
        create_project(Path(project_name), task=task)
        typer.echo(f"Created DODO project: {project_name}")
    except FileExistsError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def list(
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Path to search for DODO projects."),
) -> None:
    """List all DODO projects in the current directory or specified path."""
    search_path = path or Path.cwd()
    
    if not search_path.exists():
        typer.echo(f"Error: Path {search_path} does not exist", err=True)
        raise typer.Exit(1)
    
    projects = []
    for item in search_path.iterdir():
        if item.is_dir() and (item / "dodo.json").exists():
            try:
                config = load_config(item)
                projects.append({
                    "name": item.name,
                    "path": item,
                    "task": config.task,
                    "version": getattr(config, 'version', 'N/A')
                })
            except Exception:
                projects.append({
                    "name": item.name,
                    "path": item,
                    "task": "unknown",
                    "version": "N/A"
                })
    
    if not projects:
        typer.echo("No DODO projects found in the current directory.")
        return
    
    typer.echo(f"Found {len(projects)} DODO project(s):\n")
    
    for project in projects:
        typer.echo(f"📁 {project['name']}")
        typer.echo(f"   Path: {project['path']}")
        typer.echo(f"   Task: {project['task']}")
        typer.echo(f"   Version: {project['version']}")
        typer.echo()


@app.command()
def delete(
    project_name: str = typer.Argument(..., help="Name of the DODO project to delete."),
    force: bool = typer.Option(False, "--force", "-f", help="Force deletion without confirmation."),
) -> None:
    """Delete a DODO project and all its contents."""
    project_path = Path(project_name)
    
    if not project_path.exists():
        typer.echo(f"Error: Project '{project_name}' does not exist", err=True)
        raise typer.Exit(1)
    
    if not (project_path / "dodo.json").exists():
        typer.echo(f"Error: '{project_name}' is not a valid DODO project", err=True)
        raise typer.Exit(1)
    
    if not force:
        typer.echo(f"⚠️  This will permanently delete the project '{project_name}' and all its contents!")
        if not typer.confirm("Are you sure you want to continue?"):
            typer.echo("Deletion cancelled.")
            return
    
    try:
        import shutil
        shutil.rmtree(project_path)
        typer.echo(f"✅ Successfully deleted DODO project: {project_name}")
    except Exception as e:
        typer.echo(f"Error: Failed to delete project: {e}", err=True)
        raise typer.Exit(1)


@app.command("import")
def import_command(
    rosbag_file: Path = typer.Argument(..., help="Path to a ROS bag, JSON log, JSONL log, or mock log."),
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
) -> None:
    root = project or find_project_root()
    config = load_config(root)
    summary = import_log(rosbag_file, root, config)
    typer.echo(f"Imported {summary.total_messages} messages from {rosbag_file}")


@app.command("show-metadata")
def show_metadata_command(
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
) -> None:
    """Display DODO dataset metadata."""
    root = project or find_project_root()
    metadata_file = root / "dataset" / "metadata" / "metadata.json"
    
    if not metadata_file.exists():
        typer.echo(f"No metadata found for project at {root}")
        typer.echo("Run 'dodo generate-metadata' first to create metadata.")
        raise typer.Exit(1)
    
    import json
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Display key metadata information
    typer.echo(f"Dataset Metadata:")
    typer.echo(f"Name: {metadata['dataset_name']}")
    typer.echo(f"Task: {metadata['task']}")
    typer.echo(f"Frames: {metadata['number_of_frames']}")
    typer.echo(f"Duration: {metadata['duration']}s")
    typer.echo(f"FPS: {metadata['fps']}")
    typer.echo(f"Sensors: {', '.join(metadata['sensors_used'])}")
    
    # Show frame summary
    typer.echo(f"\nFrame Summary:")
    for i, frame in enumerate(metadata['frames']):
        typer.echo(f"Frame {i+1}: {frame['timestamp']}s")
        if frame.get('camera'):
            typer.echo(f"  Camera: {frame['camera']}")
        if frame.get('imu'):
            if isinstance(frame['imu'], dict):
                acc = frame['imu'].get('linear_acceleration', 'N/A')
                typer.echo(f"  IMU: acc={acc}")
            else:
                typer.echo(f"  IMU: {frame['imu']}")
        if frame.get('action'):
            if isinstance(frame['action'], dict):
                linear = frame['action'].get('linear', 'N/A')
                typer.echo(f"  Action: linear={linear}")
            else:
                typer.echo(f"  Action: {frame['action']}")


@app.command("generate-metadata")
def generate_metadata_command(
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
) -> None:
    root = project or find_project_root()
    config = load_config(root)
    metadata = generate_metadata(root, config)
    typer.echo(f"Generated metadata for {metadata.number_of_frames} aligned frames")


@app.command()
def validate(
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
) -> None:
    root = project or find_project_root()
    report = validate_dataset(root)
    if report.valid:
        typer.echo("Dataset is valid")
        return
    for error in report.errors:
        typer.echo(f"ERROR: {error}", err=True)
    raise typer.Exit(code=1)


@app.command()
def export(
    output_path: Path = typer.Argument(..., help="Destination path for the structured dataset."),
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
    overwrite: bool = typer.Option(False, "--overwrite", "-f", help="Overwrite existing output directory."),
) -> None:
    root = project or find_project_root()
    
    # Check if output path already exists
    if output_path.exists() and not overwrite:
        typer.echo(f"Error: Output path '{output_path}' already exists!", err=True)
        typer.echo("Choose a different name or use --overwrite/-f to replace it.")
        typer.echo(f"Examples:")
        typer.echo(f"  python -m dodo export {output_path}_new --project {root.name}")
        typer.echo(f"  python -m dodo export {output_path} --project {root.name} --overwrite")
        raise typer.Exit(1)
    
    try:
        exported = export_dataset(root, output_path, overwrite=overwrite)
        typer.echo(f"Exported dataset to {exported}")
    except FileExistsError as e:
        typer.echo(f"Error: {e}", err=True)
        typer.echo("Use --overwrite/-f to replace the existing directory.")
        raise typer.Exit(1)


@app.command()
def filter(
    filter_type: str = typer.Argument(..., help="Type of filtering to perform: 'frames' or 'messages'"),
    project: Optional[Path] = typer.Option(None, "--project", "-p", help="DODO project root.", is_flag=False),
) -> None:
    """Remove duplicate data from the dataset."""
    
    # Check authentication
    current_user = security_manager.get_current_user()
    if not current_user:
        typer.echo("Error: Authentication required. Please run 'dodo login' first.", err=True)
        raise typer.Exit(1)
    
    # Validate filter type first
    if filter_type not in ["frames", "messages"]:
        typer.echo(f"Error: Invalid filter type '{filter_type}'", err=True)
        typer.echo("Valid options are: 'frames' or 'messages'")
        raise typer.Exit(1)
    
    root = project or find_project_root()
    config = load_config(root)
    
    if filter_type == "frames":
        try:
            result = remove_duplicate_frames(root, config)
            typer.echo(f"✅ Filtered duplicate frames:")
            typer.echo(f"   Original frames: {result['original_frames']}")
            typer.echo(f"   Filtered frames: {result['filtered_frames']}")
            typer.echo(f"   Removed frames: {result['removed_frames']}")
            typer.echo(f"   Dataset duration: {result['duration']:.2f}s")
        except FileNotFoundError as e:
            typer.echo(f"Error: {e}", err=True)
            typer.echo("Run 'dodo generate-metadata' first to create metadata.")
            raise typer.Exit(1)
    
    elif filter_type == "messages":
        try:
            result = remove_duplicate_messages(root, config)
            typer.echo(f"✅ Filtered duplicate messages:")
            typer.echo(f"   Original messages: {result['original_messages']}")
            typer.echo(f"   Filtered messages: {result['filtered_messages']}")
            typer.echo(f"   Removed messages: {result['removed_messages']}")
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)


@app.command()
def login(
    username: str = typer.Option(..., "--username", "-u", help="Username for login."),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Password (will prompt if not provided)."),
) -> None:
    """Login to DODO with authentication."""
    
    if password is None:
        password = getpass.getpass("Enter password: ")
    
    try:
        user_data = security_manager.authenticate(username, password)
        if user_data:
            typer.echo(f"✅ Successfully logged in as {username}")
            typer.echo(f"🔑 API Key: {user_data['api_key']}")
            typer.echo("⚠️  Keep your API key secure and do not share it.")
        else:
            typer.echo("❌ Invalid username or password", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def logout() -> None:
    """Logout from current DODO session."""
    
    if security_manager.logout():
        typer.echo("✅ Successfully logged out")
    else:
        typer.echo("No active session found")


@app.command()
def register(
    username: str = typer.Option(..., "--username", "-u", help="Username for new account."),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email address (optional)."),
) -> None:
    """Register a new DODO account."""
    
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        typer.echo("❌ Passwords do not match", err=True)
        raise typer.Exit(1)
    
    if len(password) < 8:
        typer.echo("❌ Password must be at least 8 characters", err=True)
        raise typer.Exit(1)
    
    try:
        if security_manager.create_user(username, password, email):
            typer.echo(f"✅ Successfully created account for {username}")
            typer.echo("You can now login with: dodo login --username <username>")
        else:
            typer.echo(f"❌ Username '{username}' already exists", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def whoami() -> None:
    """Show current logged in user."""
    
    current_user = security_manager.get_current_user()
    if current_user:
        api_key = security_manager.get_user_api_key(current_user)
        typer.echo(f"👤 User: {current_user}")
        typer.echo(f"🔑 API Key: {api_key}")
    else:
        typer.echo("Not logged in. Use 'dodo login' to authenticate.")


@app.command()
def change_password(
    username: Optional[str] = typer.Option(None, "--username", "-u", help="Username (defaults to current user)."),
) -> None:
    """Change user password."""
    
    current_user = security_manager.get_current_user()
    if not current_user and not username:
        typer.echo("Error: Authentication required. Please run 'dodo login' first.", err=True)
        raise typer.Exit(1)
    
    target_username = username or current_user
    
    old_password = getpass.getpass("Enter current password: ")
    new_password = getpass.getpass("Enter new password: ")
    confirm_password = getpass.getpass("Confirm new password: ")
    
    if new_password != confirm_password:
        typer.echo("❌ Passwords do not match", err=True)
        raise typer.Exit(1)
    
    if len(new_password) < 8:
        typer.echo("❌ Password must be at least 8 characters", err=True)
        raise typer.Exit(1)
    
    try:
        if security_manager.change_password(target_username, old_password, new_password):
            typer.echo("✅ Password changed successfully")
        else:
            typer.echo("❌ Invalid current password", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    
    

def main() -> None:
    app()


if __name__ == "__main__":
    main()
