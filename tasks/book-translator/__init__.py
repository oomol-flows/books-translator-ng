#region generated meta
import typing
from oocana import LLMModelOptions
class Inputs(typing.TypedDict):
    source_epub: str
    target_language: typing.Literal["English", "Chinese", "Spanish", "French", "German", "Japanese", "Korean", "Portuguese", "Russian", "Italian", "Arabic", "Hindi"]
    submit_mode: typing.Literal["APPEND_BLOCK", "REPLACE"]
    concurrency: int
    max_group_tokens: int
    translated_path: str | None
    custom_prompt: str | None
    llm: LLMModelOptions
class Outputs(typing.TypedDict):
    translated_path: typing.NotRequired[str]
#endregion

from oocana import Context
from pathlib import Path
from epub_translator import LLM, translate, SubmitKind



async def main(params: Inputs, context: Context) -> Outputs:
    llm_config = params["llm"]
    llm_key = await context.oomol_token()
    llm_url = context.oomol_llm_env.get("base_url_v1")
    llm_model = llm_config.get("model", "oomol-chat")
    translation_llm = load_llm(
        key=llm_key,
        url=llm_url,
        model=llm_model,
        temperature=llm_config.get("temperature", 0.8),
        top_p=llm_config.get("top_p", 0.6),
    )
    fill_llm = load_llm(
        key=llm_key,
        url=llm_url,
        model=llm_model,
        temperature=(0.2, 0.9),
        top_p=(0.9, 1.0),
    )
    def on_progress(progress: float):
        progress_percent = int(progress * 100)
        context.report_progress(progress_percent)

    source_path = Path(params["source_epub"])
    translated_path = params.get("translated_path")
    target_language = params["target_language"]

    if translated_path:
        translated_path = Path(translated_path)
    else:
        source_name = source_path.stem
        output_filename = f"{source_name}_{target_language}.epub"
        translated_path = Path(source_path.parent) / output_filename
        translated_path = get_unique_path(translated_path)

    translated_path.parent.mkdir(parents=True, exist_ok=True)

    translate(
        translation_llm=translation_llm,
        fill_llm=fill_llm,
        source_path=source_path,
        target_path=translated_path,
        target_language=target_language,
        submit=SubmitKind[params["submit_mode"]],
        user_prompt=params.get("custom_prompt", None),
        max_group_tokens=params["max_group_tokens"],
        concurrency=params["concurrency"],
        on_progress=on_progress,
    )
    context.report_progress(100)

    return { "translated_path": str(translated_path) }

def load_llm(
    key: str,
    url: str,
    model: str,
    temperature: float | tuple[float, float],
    top_p: float | tuple[float, float],
) -> LLM:
    return LLM(
        key=key,
        url=url,
        model=model,
        token_encoding="o200k_base",
        timeout=360.0,
        retry_times=10,
        retry_interval_seconds=0.75,
        temperature=temperature,
        top_p=top_p,
    )


def get_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1
