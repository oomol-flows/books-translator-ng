#region generated meta
import typing
from oocana import LLMModelOptions
class Inputs(typing.TypedDict):
    source_epub: str
    target_language: typing.Literal["English", "Chinese", "Spanish", "French", "German", "Japanese", "Korean", "Portuguese", "Russian", "Italian", "Arabic", "Hindi"]
    output_path: str | None
    llm: LLMModelOptions
    custom_prompt: str | None
    max_group_tokens: int
    max_retries: int
class Outputs(typing.TypedDict):
    translated_file: typing.NotRequired[str]
    success: typing.NotRequired[bool]
#endregion

from oocana import Context
from pathlib import Path
from epub_translator import LLM, translate


async def main(params: Inputs, context: Context) -> Outputs:
    """
    Translate an EPUB file to the target language using LLM.

    Args:
        params: Input parameters including source file, target language, and LLM config
        context: OOMOL context for accessing LLM credentials and reporting progress

    Returns:
        Dictionary containing the translated file path and success status
    """
    try:
        # Get LLM configuration
        llm_config = params["llm"]

        # Initialize LLM client with OOMOL credentials
        llm = LLM(
            key=await context.oomol_token(),
            url=context.oomol_llm_env.get("base_url_v1"),
            model=llm_config.get("model", "oomol-chat"),
            token_encoding="o200k_base",
            cache_path=None,  # Disable caching
            timeout=300.0,
            retry_times=params["max_retries"],
            retry_interval_seconds=6.0,
        )

        # Define progress callback
        def on_progress(progress: float):
            """Report translation progress to OOMOL UI"""
            progress_percent = int(progress * 100)
            context.report_progress(progress_percent)

        # Get paths
        source_path = Path(params["source_epub"])

        # Use output_path if provided, otherwise default to session_dir
        if params.get("output_path"):
            output_path = Path(params["output_path"])
        else:
            # Generate output filename based on source and target language
            source_name = source_path.stem
            target_lang = params["target_language"]
            output_filename = f"{source_name}_{target_lang}.epub"
            output_path = Path(context.session_dir) / output_filename

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get optional custom prompt
        user_prompt = params.get("custom_prompt")

        # Perform translation
        translate(
            llm=llm,
            source_path=source_path,
            target_path=output_path,
            target_language=params["target_language"],
            user_prompt=user_prompt if user_prompt else None,
            max_retries=params["max_retries"],
            max_group_tokens=params["max_group_tokens"],
            on_progress=on_progress,
        )

        # Report completion
        context.report_progress(100)

        return {
            "translated_file": str(output_path),
            "success": True
        }

    except Exception as e:
        # Report error and return failure status
        raise RuntimeError(f"Translation failed: {str(e)}")
