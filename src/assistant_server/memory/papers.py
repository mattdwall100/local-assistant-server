from ..core.logging import get_logger

from pydantic import BaseModel, Field


logger = get_logger(__name__)


class Paper(BaseModel):
    internal_id: int = Field(ge=1, le=5)
    title: str
    summary: str
    id: str
    organization: str | None


class PapersManager:
    def __init__(self) -> None:
        self._papers: list[Paper] = []
        self._staged: Paper | None = None

    # STARTUP METHODS (used by FETCH TOOLS) -----------------------------------------
    def save_paper(self, **kwargs) -> None:
        # Run in try catch, if no error, success

        if len(self._papers) >= 5:
            logger.info(
                f"set_paper failed | rejected set as paper list has length: {len(self._papers)}"
            )
            raise AttributeError
        try:
            paper = Paper(**kwargs)
        except Exception as e:
            error_message = "set_paper failed | the passed kwargs did not pass validation: "
            for k, v in kwargs.items():
                error_message += f"{k}={v} ,"
            error_message += f"exception={e}"
            logger.error(error_message)
            raise ValueError(error_message)

        self._papers.append(paper)

    # QUERY METHODS -----------------------------------------------------------------
    def list_titles(self) -> list[str]:
        if len(self._papers) != 5:
            logger.info("get_titles failed | couldnt find all papers")
            raise AttributeError("get_titles failed | couldnt find all papers")

        return [paper.title for paper in self._papers]

    def get_summary(self, internal_id: int) -> str:
        if not internal_id in [1, 2, 3, 4, 5]:
            logger.error(
                f"get_summary failed | internal_id must be in [1, 2, 3, 4, 5], internal_id={internal_id}"
            )
            raise ValueError("internal_id must be in [1, 2, 3, 4, 5]")

        for paper in self._papers:
            if paper.internal_id == internal_id:
                return paper.summary

        logger.info("get_summary failed | couldnt find the paper")
        raise AttributeError("get_ssummary failed | couldnt find paper")

    def get_staged_title(self) -> str:
        if not self._staged:
            logger.info("get_staged_title failed | No paper was staged")
            raise AttributeError("get_staged_title failed | No paper was staged")

        return self._staged.title

    def get_staged_to_print(self) -> Paper:
        if not self._staged:
            logger.info("get_staged_to_print failed | No paper was staged")
            raise AttributeError("get_staged_to_print failed | No paper was staged")

        return self._staged

    # ACT METHODS -------------------------------------------------------------------
    def stage_paper(self, internal_id: int) -> None:
        if not internal_id in [1, 2, 3, 4, 5]:
            logger.error(
                f"stage_paper failed | internal_id must be in [1, 2, 3, 4, 5], internal_id={internal_id}"
            )
            raise ValueError("internal_id must be in [1, 2, 3, 4, 5]")

        for paper in self._papers:
            if paper.internal_id == internal_id:
                self._staged = paper
                return

        logger.info("stage_paper failed | couldnt find paper")
        raise AttributeError("get_staged_title failed | couldnt find paper")

    def remove_staged(self) -> None:
        self._staged = None
