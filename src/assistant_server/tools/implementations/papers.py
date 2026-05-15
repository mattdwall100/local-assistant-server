from ...memory.store import MemoryStore
from huggingface_hub import HfApi

from ...core.logging import get_logger


logger = get_logger(__name__)


# Fetch ----------------------------------------


def get_papers(**kwargs) -> str:
    """
    Fetch the current trending Hugging Face daily papers and store them for this session.

    Use this tool when the user asks to fetch, refresh, load, or retrieve the latest AI papers.
    The tool stores the papers in session memory with internal IDs so later tools can list,
    summarize, stage, or print a selected paper. It also returns them so you can tell the user.

    Args:
        No arguements

    Returns:
        str: A numbered list of the paper titles that were successfully fetched and stored.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")
    
    papers_manager = memory.get_papers_manager(session_id)

    api = HfApi()
    sorted_papers = api.list_daily_papers(sort="trending", limit=50)

    recorded_titles = []
    i = 1
    for paper in sorted_papers:
        paper_info = vars(paper)

        if not (paper_info["id"] and paper_info["title"] and paper_info["summary"]):
            continue
        if paper_info["organization"]:
            paper_info["organization"] = paper_info["organization"].name

        paper_info["internal_id"] = i
        try:
            papers_manager.save_paper(**paper_info)
        except Exception as e:
            logger.warning(f"get_papers | save_papers failed, exc={e}")
        else:
            i += 1
            recorded_titles.append(paper_info["title"])
        if i > 5:
            break

    return " ".join([f"{r+1}: {title}." for r, title in enumerate(recorded_titles)])


# Query ----------------------------------------


def list_titles(**kwargs) -> str:
    """
    List the titles of the currently stored AI papers for this session.

    Use this tool when the user asks to list, repeat, show, or remind them of the
    currently fetched papers. Papers are returned with their internal IDs so they
    can later be referenced by other paper tools.

    Args:
        No arguements

    Returns:
        str: A numbered list of the currently stored paper titles, or an error message
        if no papers have been fetched yet.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")

    papers_manager = memory.get_papers_manager(session_id)
    try:
        titles = papers_manager.list_titles()
    except AttributeError:
        return "ERROR: Need to get papers before listing them"

    return " ".join([f"{r+1}: {title}." for r, title in enumerate(titles)])


def get_summary(internal_id: int, **kwargs) -> str:
    """
    Retrieve the full summary for one of the stored AI papers.

    Use this tool when the user asks for the summary, details, explanation,
    or overview of a previously fetched paper by its internal ID.

    Args:
        internal_id: The numbered paper ID shown to the user, integer between 1 and 5.

    Returns:
        str: The full paper summary for the requested paper, or an error message
        if the paper ID is invalid or no matching paper exists.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")

    papers_manager = memory.get_papers_manager(session_id)
    try:
        summary = papers_manager.get_summary(internal_id)
    except ValueError:
        return f"ERROR: Invalid internal_id used, must be between 1 and 5, tried with {internal_id}"
    except AttributeError:
        return f"ERROR: Couldnt find all the paper for id={internal_id}"

    return summary


def get_staged_title(**kwargs) -> str:
    """
    Retrieve the title of the currently staged AI paper.

    Use this tool when the user asks which paper is staged, selected, prepared,
    or ready for a later action such as printing.

    Args:
        No arguements

    Returns:
        str: The title of the currently staged paper, or an error message if no paper is staged.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")

    papers_manager = memory.get_papers_manager(session_id)
    try:
        staged_title = papers_manager.get_staged_title()
    except AttributeError:
        return "ERROR: No paper is staged"

    return staged_title


# Act ------------------------------------------


def stage_paper(internal_id: int, **kwargs) -> str:
    """
    Stage a stored AI paper for a later action such as printing.

    Use this tool when the user asks to select, stage, prepare, or choose one of
    the fetched papers by its internal ID. The staged paper can then be checked
    or used by later tools.

    Args:

        internal_id: The numbered paper ID shown to the user, integer between 1 and 5.

    Returns:
        str: A success message confirming which paper ID was staged, or an error
        message if the ID is invalid or no matching paper exists.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")

    papers_manager = memory.get_papers_manager(session_id)
    try:
        papers_manager.stage_paper(internal_id)
    except ValueError:
        return f"ERROR: Invalid internal_id used, must be between 1 and 5, tried with {internal_id}"
    except AttributeError:
        return f"ERROR: Couldnt find the paper for id={internal_id}"

    return f"Successfully staged paper with id={internal_id}"


def print_paper(**kwargs) -> str:
    """
    Print the currently staged AI paper.

    Use this tool when the user asks to print the selected, staged, or prepared
    paper. The paper must already have been staged using the stage paper tool.

    Returns:
        str: A success message if the staged paper was sent to the printer, or an
        error message if no paper is staged, the PDF cannot be downloaded, or the
        print command fails.
    """
    memory = kwargs.get("memory")
    session_id = kwargs.get("session_id")

    papers_manager = memory.get_papers_manager(session_id)
    try:
        paper = papers_manager.get_staged_to_print()
    except AttributeError:
        return "ERROR: No paper is staged"

    arxiv_id = paper.id
    title = paper.title
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    return f"attempting print of {papers_manager._staged.title}..."
    # call PM method

    # handle errors

    # .remove_staged()

    # Send print request

    # return string.
