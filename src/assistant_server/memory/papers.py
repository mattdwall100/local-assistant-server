
class Paper(BaseModel):
    internal_id: int = Field(ge=1, le=3)

    title: str
    ai_summary: str
    summary: str
    arxiv_id: str


class PapersManager():
    def __init__(self) -> None:
        self._papers: list[Paper] = []
        self._staged: Paper | None = None

    # STARTUP METHODS (used by FETCH TOOLS) -----------------------------------------
    def save_paper(self, kwargs) -> None:
        # Run in try catch, if no error, success

        if len(self._papers) >= 3:
            logger.info(f"set_paper failed | rejected set as paper list has length: {len(self._papers)}")
            raise Error
        try:
            paper = Paper(**kwargs)
        except Exception as e:
            error_message = "set_paper failed | the passed kwargs did not pass validation: "
            for k, v in kwargs.items():
                error_message += f"{k}={v} ,"
            error_message += f"exception={e}"
            logger.error(error_message)
            raise Error(error_message)

        self._papers.append(paper)

    # QUERY METHODS -----------------------------------------------------------------
    def list_titles(self) -> dict[str, str]:
        titles = dict[str, str]
        for paper, i in enumerate(self._papers):
            titles[f"paper{i+1}"] = paper.title
        return list_titles
            
    def get_summary(self, internal_id: int) -> str:
        if not internal_id in [1, 2, 3]:
            logger.error(f"get_summary failed | internal_id must be in [1, 2, 3], internal_id={internal_id}")
            raise ValueError("internal_id must be in [1, 2, 3]")
        for paper in self._papers:
            if paper.internal_id == internal_id:
                return paper.summary

    def get_staged(self) -> str:
        if not self._staged:
            logger.info("get_staged failed | No paper was staged")
            return "ERROR: No paper is currently staged, stage a paper and try again"
        return self._staged.title

    def get_staged_to_print(self) -> Paper:
        if not self._staged:
            logger.info("get_staged_to_print failed | No paper was staged")
            return "ERROR: No paper is currently staged, stage a paper and try again"
            # Raise an error, the tool will catch it (tool handles formulating response, paper manager doesnt know what will use it)
        
    # ACT METHODS -------------------------------------------------------------------
    def stage_paper(self, internal_id: int) -> str:
        if not internal_id in [1, 2, 3]:
            logger.error(f"stage_paper failed | internal_id must be in [1, 2, 3], internal_id={internal_id}")
            raise ValueError("internal_id must be in [1, 2, 3]")
        for paper in self._papers:
            if paper.internal_id == internal_id:    